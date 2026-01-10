// Audiobook Narrator App
class AudiobookNarrator {
    constructor() {
        this.bookText = '';
        this.currentPosition = 0;
        this.isPlaying = false;
        this.isPaused = false;
        this.utterance = null;
        this.synth = window.speechSynthesis;
        this.voices = [];
        this.bookFileName = '';

        this.initElements();
        this.initEventListeners();
        this.loadVoices();
        this.loadSavedState();
    }

    initElements() {
        // File upload elements
        this.fileInput = document.getElementById('fileInput');
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInfo = document.getElementById('fileInfo');

        // Book display elements
        this.bookSection = document.getElementById('bookSection');
        this.bookTitle = document.getElementById('bookTitle');
        this.bookContent = document.getElementById('bookContent');
        this.progressText = document.getElementById('progressText');

        // Control elements
        this.controlsSection = document.getElementById('controlsSection');
        this.playPauseBtn = document.getElementById('playPauseBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.speedControl = document.getElementById('speedControl');
        this.speedValue = document.getElementById('speedValue');
        this.pitchControl = document.getElementById('pitchControl');
        this.pitchValue = document.getElementById('pitchValue');
        this.voiceSelect = document.getElementById('voiceSelect');
        this.progressFill = document.getElementById('progressFill');
        this.loadNewBtn = document.getElementById('loadNewBtn');

        // Instructions
        this.instructions = document.getElementById('instructions');

        // Icons
        this.playIcon = this.playPauseBtn.querySelector('.play-icon');
        this.pauseIcon = this.playPauseBtn.querySelector('.pause-icon');
    }

    initEventListeners() {
        // File upload
        this.fileInput.addEventListener('change', (e) => this.handleFileUpload(e));

        // Drag and drop
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadArea.style.borderColor = 'var(--primary-color)';
        });

        this.uploadArea.addEventListener('dragleave', () => {
            this.uploadArea.style.borderColor = 'var(--border-color)';
        });

        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadArea.style.borderColor = 'var(--border-color)';
            if (e.dataTransfer.files.length) {
                this.fileInput.files = e.dataTransfer.files;
                this.handleFileUpload({ target: this.fileInput });
            }
        });

        // Playback controls
        this.playPauseBtn.addEventListener('click', () => this.togglePlayPause());
        this.stopBtn.addEventListener('click', () => this.stop());
        this.loadNewBtn.addEventListener('click', () => this.loadNewBook());

        // Settings controls
        this.speedControl.addEventListener('input', (e) => {
            this.speedValue.textContent = e.target.value + 'x';
            if (this.utterance) {
                this.updateSpeechSettings();
            }
        });

        this.pitchControl.addEventListener('input', (e) => {
            this.pitchValue.textContent = e.target.value;
            if (this.utterance) {
                this.updateSpeechSettings();
            }
        });

        this.voiceSelect.addEventListener('change', () => {
            if (this.utterance) {
                this.updateSpeechSettings();
            }
        });

        // Speech synthesis events
        if (this.synth) {
            this.synth.addEventListener('voiceschanged', () => this.loadVoices());
        }
    }

    loadVoices() {
        this.voices = this.synth.getVoices();
        this.voiceSelect.innerHTML = '';

        if (this.voices.length === 0) {
            const option = document.createElement('option');
            option.textContent = 'Loading voices...';
            this.voiceSelect.appendChild(option);
            return;
        }

        this.voices.forEach((voice, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = `${voice.name} (${voice.lang})`;
            if (voice.default) {
                option.selected = true;
            }
            this.voiceSelect.appendChild(option);
        });

        // Load saved voice preference
        const savedVoice = localStorage.getItem('preferredVoice');
        if (savedVoice) {
            this.voiceSelect.value = savedVoice;
        }
    }

    async handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        this.bookFileName = file.name;

        try {
            const text = await this.readFile(file);
            this.bookText = this.cleanText(text);

            if (this.bookText.length === 0) {
                alert('The file appears to be empty or could not be read.');
                return;
            }

            this.currentPosition = 0;
            this.displayBook();
            this.saveState();

            // Show success message
            this.fileInfo.textContent = `✓ Loaded: ${file.name} (${this.formatFileSize(file.size)})`;
            this.fileInfo.classList.add('show');

            // Hide instructions, show controls
            this.instructions.style.display = 'none';
            this.bookSection.style.display = 'block';
            this.controlsSection.style.display = 'block';
            this.playPauseBtn.disabled = false;
            this.stopBtn.disabled = false;

        } catch (error) {
            alert('Error reading file: ' + error.message);
        }
    }

    readFile(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = (e) => reject(e);
            reader.readAsText(file);
        });
    }

    cleanText(text) {
        // Remove excessive whitespace and clean up text
        return text
            .replace(/\r\n/g, '\n')
            .replace(/\n{3,}/g, '\n\n')
            .replace(/\t/g, ' ')
            .replace(/ {2,}/g, ' ')
            .trim();
    }

    displayBook() {
        this.bookTitle.textContent = this.bookFileName;

        // Display first 500 characters as preview
        const preview = this.bookText.substring(0, 500) + '...';
        this.bookContent.textContent = preview;

        this.updateProgress();
    }

    togglePlayPause() {
        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }

    play() {
        if (this.isPaused && this.utterance) {
            // Resume from pause
            this.synth.resume();
            this.isPlaying = true;
            this.isPaused = false;
            this.updatePlayPauseButton();
            return;
        }

        // Start new narration
        const textToSpeak = this.bookText.substring(this.currentPosition);

        if (textToSpeak.length === 0) {
            alert('End of book reached!');
            this.currentPosition = 0;
            this.updateProgress();
            return;
        }

        this.utterance = new SpeechSynthesisUtterance(textToSpeak);

        // Apply settings
        this.utterance.rate = parseFloat(this.speedControl.value);
        this.utterance.pitch = parseFloat(this.pitchControl.value);

        const selectedVoice = this.voiceSelect.value;
        if (selectedVoice && this.voices[selectedVoice]) {
            this.utterance.voice = this.voices[selectedVoice];
            localStorage.setItem('preferredVoice', selectedVoice);
        }

        // Event handlers
        this.utterance.onboundary = (event) => {
            this.currentPosition += event.charIndex;
            this.updateProgress();
            this.saveState();
        };

        this.utterance.onend = () => {
            this.isPlaying = false;
            this.isPaused = false;
            this.currentPosition = this.bookText.length;
            this.updateProgress();
            this.updatePlayPauseButton();
            this.saveState();
        };

        this.utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event);
            this.isPlaying = false;
            this.isPaused = false;
            this.updatePlayPauseButton();
        };

        this.synth.speak(this.utterance);
        this.isPlaying = true;
        this.isPaused = false;
        this.updatePlayPauseButton();
    }

    pause() {
        if (this.synth.speaking) {
            this.synth.pause();
            this.isPlaying = false;
            this.isPaused = true;
            this.updatePlayPauseButton();
        }
    }

    stop() {
        this.synth.cancel();
        this.isPlaying = false;
        this.isPaused = false;
        this.utterance = null;
        this.updatePlayPauseButton();
    }

    updateSpeechSettings() {
        // Need to restart narration with new settings
        if (this.isPlaying) {
            const wasPlaying = true;
            this.stop();
            if (wasPlaying) {
                setTimeout(() => this.play(), 100);
            }
        }
    }

    updatePlayPauseButton() {
        if (this.isPlaying) {
            this.playIcon.style.display = 'none';
            this.pauseIcon.style.display = 'block';
            this.playPauseBtn.querySelector('span').textContent = 'Pause';
        } else {
            this.playIcon.style.display = 'block';
            this.pauseIcon.style.display = 'none';
            this.playPauseBtn.querySelector('span').textContent = 'Play';
        }
    }

    updateProgress() {
        const percentage = this.bookText.length > 0
            ? Math.round((this.currentPosition / this.bookText.length) * 100)
            : 0;

        this.progressText.textContent = `${percentage}% complete`;
        this.progressFill.style.width = percentage + '%';
    }

    loadNewBook() {
        this.stop();
        this.bookText = '';
        this.currentPosition = 0;
        this.bookFileName = '';

        this.bookSection.style.display = 'none';
        this.controlsSection.style.display = 'none';
        this.instructions.style.display = 'block';
        this.fileInfo.classList.remove('show');
        this.fileInput.value = '';

        localStorage.removeItem('bookState');
    }

    saveState() {
        const state = {
            bookText: this.bookText,
            currentPosition: this.currentPosition,
            bookFileName: this.bookFileName,
            speed: this.speedControl.value,
            pitch: this.pitchControl.value
        };
        localStorage.setItem('bookState', JSON.stringify(state));
    }

    loadSavedState() {
        const savedState = localStorage.getItem('bookState');
        if (savedState) {
            try {
                const state = JSON.parse(savedState);

                if (state.bookText && state.bookText.length > 0) {
                    this.bookText = state.bookText;
                    this.currentPosition = state.currentPosition || 0;
                    this.bookFileName = state.bookFileName || 'Saved Book';

                    if (state.speed) this.speedControl.value = state.speed;
                    if (state.pitch) this.pitchControl.value = state.pitch;

                    this.speedValue.textContent = this.speedControl.value + 'x';
                    this.pitchValue.textContent = this.pitchControl.value;

                    this.displayBook();
                    this.instructions.style.display = 'none';
                    this.bookSection.style.display = 'block';
                    this.controlsSection.style.display = 'block';
                    this.playPauseBtn.disabled = false;
                    this.stopBtn.disabled = false;

                    this.fileInfo.textContent = `✓ Resumed: ${this.bookFileName}`;
                    this.fileInfo.classList.add('show');
                }
            } catch (error) {
                console.error('Error loading saved state:', error);
            }
        }
    }

    formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Check for Speech Synthesis support
    if (!('speechSynthesis' in window)) {
        alert('Sorry, your browser does not support text-to-speech. Please try a different browser.');
        return;
    }

    // Initialize the app
    window.narrator = new AudiobookNarrator();

    // Register service worker for PWA
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('service-worker.js')
            .then(registration => {
                console.log('Service Worker registered:', registration);
            })
            .catch(error => {
                console.log('Service Worker registration failed:', error);
            });
    }
});

// Prevent text selection during playback
document.addEventListener('selectstart', (e) => {
    if (window.narrator && window.narrator.isPlaying) {
        e.preventDefault();
    }
});
