// UESC Marathon Task Visualizer
// Parallel thread execution monitor

class TaskVisualizer {
    constructor() {
        this.threads = new Map();
        this.completedCount = 0;
        this.startTime = Date.now();
        this.threadIdCounter = 1;

        this.initializeUI();
        this.startUptime();
    }

    initializeUI() {
        // Button handlers
        document.getElementById('add-task-btn').addEventListener('click', () => {
            this.createThread('Single Task Execution', 3000);
        });

        document.getElementById('parallel-btn').addEventListener('click', () => {
            this.createParallelThreads();
        });

        document.getElementById('clear-btn').addEventListener('click', () => {
            this.clearLogs();
        });
    }

    createThread(name, duration = null) {
        const threadId = this.threadIdCounter++;
        const actualDuration = duration || Math.random() * 5000 + 2000;

        const thread = {
            id: threadId,
            name: name,
            status: 'running',
            progress: 0,
            startTime: Date.now(),
            duration: actualDuration
        };

        this.threads.set(threadId, thread);
        this.renderThread(thread);
        this.addTimelineEvent(`Thread ${threadId} initialized: ${name}`, 'running');
        this.updateStatusBar();

        // Simulate task execution
        this.executeThread(thread);
    }

    executeThread(thread) {
        const interval = 50;
        const steps = thread.duration / interval;
        let currentStep = 0;

        const progressInterval = setInterval(() => {
            currentStep++;
            thread.progress = (currentStep / steps) * 100;

            if (currentStep >= steps) {
                clearInterval(progressInterval);
                this.completeThread(thread.id);
            } else {
                this.updateThreadProgress(thread.id, thread.progress);
            }
        }, interval);
    }

    completeThread(threadId) {
        const thread = this.threads.get(threadId);
        if (!thread) return;

        thread.status = 'completed';
        thread.progress = 100;

        this.updateThreadStatus(threadId);
        this.completedCount++;
        this.updateStatusBar();

        const duration = ((Date.now() - thread.startTime) / 1000).toFixed(2);
        this.addTimelineEvent(
            `Thread ${threadId} completed: ${thread.name} [${duration}s]`,
            'completed'
        );

        // Remove thread from display after delay
        setTimeout(() => {
            this.removeThread(threadId);
        }, 2000);
    }

    createParallelThreads() {
        const tasks = [
            'Read File: config.json',
            'Parse XML: slide38.xml',
            'Execute Bash: git status',
            'Grep Search: cocktail timeline',
            'Web Fetch: marathon news'
        ];

        tasks.forEach((task, index) => {
            setTimeout(() => {
                this.createThread(task, Math.random() * 4000 + 1000);
            }, index * 100);
        });

        this.addTimelineEvent(
            `Spawned ${tasks.length} parallel threads`,
            'running'
        );
    }

    renderThread(thread) {
        const container = document.getElementById('thread-container');
        const threadEl = document.createElement('div');
        threadEl.className = 'thread';
        threadEl.id = `thread-${thread.id}`;

        threadEl.innerHTML = `
            <div class="thread-header">
                <span class="thread-id">THREAD_${String(thread.id).padStart(3, '0')}</span>
                <span class="thread-status ${thread.status}">${thread.status.toUpperCase()}</span>
            </div>
            <div class="thread-name">${thread.name}</div>
            <div class="thread-progress">
                <div class="thread-progress-bar ${thread.status === 'running' ? 'active' : ''}"
                     style="width: ${thread.progress}%"></div>
            </div>
        `;

        container.insertBefore(threadEl, container.firstChild);
    }

    updateThreadProgress(threadId, progress) {
        const threadEl = document.getElementById(`thread-${threadId}`);
        if (!threadEl) return;

        const progressBar = threadEl.querySelector('.thread-progress-bar');
        progressBar.style.width = `${progress}%`;
    }

    updateThreadStatus(threadId) {
        const thread = this.threads.get(threadId);
        const threadEl = document.getElementById(`thread-${threadId}`);
        if (!threadEl || !thread) return;

        const statusEl = threadEl.querySelector('.thread-status');
        statusEl.className = `thread-status ${thread.status}`;
        statusEl.textContent = thread.status.toUpperCase();

        const progressBar = threadEl.querySelector('.thread-progress-bar');
        progressBar.classList.remove('active');
        progressBar.style.width = '100%';
    }

    removeThread(threadId) {
        const threadEl = document.getElementById(`thread-${threadId}`);
        if (threadEl) {
            threadEl.style.opacity = '0';
            threadEl.style.transform = 'translateX(-20px)';
            setTimeout(() => {
                threadEl.remove();
                this.threads.delete(threadId);
                this.updateStatusBar();
            }, 300);
        }
    }

    addTimelineEvent(description, status = 'running') {
        const timeline = document.getElementById('timeline');
        const eventEl = document.createElement('div');
        eventEl.className = `timeline-event ${status}`;

        const now = new Date();
        const timeStr = now.toLocaleTimeString('en-US', { hour12: false });

        eventEl.innerHTML = `
            <div class="timeline-time">[${timeStr}]</div>
            <div class="timeline-desc">${description}</div>
        `;

        timeline.insertBefore(eventEl, timeline.firstChild);

        // Limit timeline events
        const events = timeline.querySelectorAll('.timeline-event');
        if (events.length > 50) {
            events[events.length - 1].remove();
        }
    }

    updateStatusBar() {
        const activeThreads = Array.from(this.threads.values())
            .filter(t => t.status === 'running').length;

        document.getElementById('thread-count').textContent = activeThreads;
        document.getElementById('completed-count').textContent = this.completedCount;
    }

    startUptime() {
        setInterval(() => {
            const elapsed = Date.now() - this.startTime;
            const hours = Math.floor(elapsed / 3600000);
            const minutes = Math.floor((elapsed % 3600000) / 60000);
            const seconds = Math.floor((elapsed % 60000) / 1000);

            const uptimeStr = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
            document.getElementById('uptime').textContent = uptimeStr;
        }, 1000);
    }

    clearLogs() {
        const timeline = document.getElementById('timeline');
        const threadContainer = document.getElementById('thread-container');

        timeline.innerHTML = '';
        threadContainer.innerHTML = '';

        this.threads.clear();
        this.completedCount = 0;
        this.threadIdCounter = 1;

        this.updateStatusBar();
        this.addTimelineEvent('System logs purged', 'completed');
    }
}

// API for external integration
class TaskMonitorAPI {
    constructor(visualizer) {
        this.visualizer = visualizer;
        window.taskMonitor = this;
    }

    // Public API methods
    startTask(name, estimatedDuration = null) {
        return this.visualizer.createThread(name, estimatedDuration);
    }

    startParallelTasks(tasks) {
        tasks.forEach((task, index) => {
            setTimeout(() => {
                this.visualizer.createThread(
                    task.name,
                    task.duration || null
                );
            }, index * 100);
        });
    }

    logEvent(message, status = 'running') {
        this.visualizer.addTimelineEvent(message, status);
    }

    getStats() {
        return {
            activeThreads: Array.from(this.visualizer.threads.values())
                .filter(t => t.status === 'running').length,
            completedTasks: this.visualizer.completedCount,
            totalThreads: this.visualizer.threads.size
        };
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const visualizer = new TaskVisualizer();
    const api = new TaskMonitorAPI(visualizer);

    // Demo sequence
    setTimeout(() => {
        visualizer.addTimelineEvent('System initialized', 'completed');
        visualizer.addTimelineEvent('Cryo Archive access granted', 'completed');
    }, 500);

    console.log('UESC Task Monitor initialized');
    console.log('Use window.taskMonitor API for integration:');
    console.log('  taskMonitor.startTask("Task Name", duration)');
    console.log('  taskMonitor.logEvent("Message", "status")');
    console.log('  taskMonitor.getStats()');
});
