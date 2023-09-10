package es.us.isa.restest.util;

import org.junit.Test;

import static es.us.isa.restest.util.Timer.TestStep.*;
import static es.us.isa.restest.util.Timer.exportToCSV;
import static es.us.isa.restest.util.Timer.resetCounters;
import static junit.framework.TestCase.assertEquals;
import static junit.framework.TestCase.assertTrue;

public class TimerTest {

    @Test
    public void timerTest() throws InterruptedException {
        resetCounters();
        assertEquals("The timer should be empty", 0, Timer.getCounters().size());
        Timer.startCounting(ALL);
        Thread.sleep(500);
        Timer.startCounting(TEST_SUITE_GENERATION);
        assertEquals("The TEST_SUITE_GENERATION timer should have 1 entry", 1, Timer.getCounters().get(TEST_SUITE_GENERATION.getName()).size());
        Thread.sleep(1000);
        Timer.startCounting(TEST_SUITE_GENERATION);
        assertEquals("The TEST_SUITE_GENERATION timer should still have 1 entry", 1, Timer.getCounters().get(TEST_SUITE_GENERATION.getName()).size());
        Thread.sleep(100);
        Timer.stopCounting(TEST_SUITE_GENERATION);
        Thread.sleep(1500);
        Timer.startCounting(TEST_SUITE_EXECUTION);
        Timer.stopCounting(TEST_SUITE_EXECUTION);
        Timer.startCounting(TEST_SUITE_GENERATION);
        Thread.sleep(200);
        Timer.startCounting(TEST_SUITE_EXECUTION);
        Thread.sleep(200);
        Timer.stopCounting(TEST_SUITE_GENERATION);
        Timer.stopCounting(TEST_SUITE_EXECUTION);
        Timer.stopCounting(ALL);

        System.out.println(Timer.getCounters());
        assertEquals("The timer should have 3 counters", 3, Timer.getCounters().size());
        assertEquals("The ALL counter should have 1 entry", 1, Timer.getCounters().get(ALL.getName()).size());
        assertEquals("The TEST_SUITE_GENERATION counter should have 2 entries", 2, Timer.getCounters().get(TEST_SUITE_GENERATION.getName()).size());
        assertEquals("The TEST_SUITE_EXECUTION counter should have 2 entries", 2, Timer.getCounters().get(TEST_SUITE_EXECUTION.getName()).size());
        assertTrue("The ALL counter should have lasted 3000ms at least", Timer.getCounters().get(ALL.getName()).get(0) >= 3400);
        assertTrue("The first TEST_SUITE_GENERATION counter should have lasted 100ms at least", Timer.getCounters().get(TEST_SUITE_GENERATION.getName()).get(0) >= 100);
        assertTrue("The first TEST_SUITE_EXECUTION counter should have lasted 0ms at least", Timer.getCounters().get(TEST_SUITE_EXECUTION.getName()).get(0) >= 0);
        assertTrue("The second TEST_SUITE_GENERATION counter should have lasted 1000ms at least", Timer.getCounters().get(TEST_SUITE_GENERATION.getName()).get(1) >= 400);
        assertTrue("The second TEST_SUITE_EXECUTION counter should have lasted 0ms at least", Timer.getCounters().get(TEST_SUITE_EXECUTION.getName()).get(1) >= 200);

        String timePath = PropertyManager.readProperty("data.tests.dir") + "/" + PropertyManager.readProperty("data.tests.time");
        FileManager.createDir(PropertyManager.readProperty("data.tests.dir"));
        exportToCSV(timePath, 2);
        assertTrue("The time report should have been created in " + timePath, FileManager.checkIfExists(timePath));

    }


}
