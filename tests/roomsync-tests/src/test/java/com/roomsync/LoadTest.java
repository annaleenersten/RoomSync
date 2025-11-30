package com.roomsync;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class LoadTest {

    // Change this if your port/URL is different
    private static final String BASE_URL = "http://localhost:5001/base";

    @Test
    public void testBasicUptime() throws Exception {
        URL url = new URL(BASE_URL);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        int status = conn.getResponseCode();
        conn.disconnect();

        Assertions.assertEquals(200, status,
                "Expected HTTP 200 from /base for basic uptime check");
    }

    @Test
    public void test500SimultaneousUsers() throws Exception {
        int totalUsers = 500;

        ExecutorService executor = Executors.newFixedThreadPool(100);
        List<Callable<Boolean>> tasks = new ArrayList<>();

        for (int i = 0; i < totalUsers; i++) {
            tasks.add(() -> {
                try {
                    URL url = new URL(BASE_URL);
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setRequestMethod("GET");
                    conn.setConnectTimeout(2000);
                    conn.setReadTimeout(2000);

                    int status = conn.getResponseCode();
                    conn.disconnect();
                    return status == 200;
                } catch (Exception e) {
                    return false;
                }
            });
        }

        List<Future<Boolean>> futures = executor.invokeAll(tasks);
        executor.shutdown();

        int successCount = 0;
        for (Future<Boolean> f : futures) {
            if (Boolean.TRUE.equals(f.get())) {
                successCount++;
            }
        }

        // Require at least 450/500 successful responses (90%)
        Assertions.assertTrue(
                successCount >= 450,
                "Expected at least 450 successful responses, got " + successCount
        );
    }
}