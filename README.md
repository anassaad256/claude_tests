# 📚 Audiobook Narrator

A Progressive Web App (PWA) that turns your text files into audiobooks using text-to-speech technology. Listen to any book on your phone!

## Features

- 📱 **Mobile-First Design** - Optimized for smartphones and tablets
- 🔊 **Text-to-Speech** - High-quality narration using your device's TTS engine
- ⚙️ **Customizable Playback** - Adjust speed, pitch, and voice
- 💾 **Auto-Save Progress** - Automatically remembers where you left off
- 📲 **Installable** - Add to your phone's home screen like a native app
- 🌙 **Dark Mode** - Automatically adapts to your system preference
- 📴 **Offline Support** - Works without internet once installed

## How to Use

### On Your Phone

1. **Access the App**
   - Open your phone's web browser (Safari, Chrome, etc.)
   - Navigate to where this app is hosted
   - Or open the `index.html` file if you have it locally

2. **Install to Home Screen**

   **iPhone (Safari):**
   - Tap the Share button (square with arrow)
   - Scroll down and tap "Add to Home Screen"
   - Name it "Audiobook" and tap "Add"

   **Android (Chrome):**
   - Tap the three-dot menu
   - Select "Add to Home Screen" or "Install"
   - Tap "Add" or "Install"

3. **Upload a Book**
   - Tap the upload area
   - Select a text file (TXT format works best)
   - The app will load your book

4. **Start Listening**
   - Press the Play button
   - Adjust speed and pitch to your preference
   - Choose your preferred voice from the dropdown
   - The app will save your position automatically

### Supported File Formats

- **TXT** - Plain text files (recommended)
- **EPUB** - E-books (text content will be extracted)
- **PDF** - PDF documents (text content will be extracted)

For best results, use plain text (.txt) files.

## Controls

- **Play/Pause** - Start or pause narration
- **Stop** - Stop and reset current narration
- **Speed** - Adjust reading speed (0.5x to 2.0x)
- **Pitch** - Change voice pitch (0.5 to 2.0)
- **Voice** - Select different voices (varies by device)
- **Progress Bar** - Visual indicator of reading progress

## Features Explained

### Auto-Save
The app automatically saves:
- Your current book
- Reading position
- Speed and pitch settings

Close the app and reopen it anytime - you'll pick up right where you left off!

### Voice Selection
Different devices have different voices available:
- iOS devices typically have high-quality Siri voices
- Android devices use Google TTS voices
- Desktop browsers may have additional voices installed

### Offline Mode
Once installed as a PWA, the app works offline. However, you'll need an internet connection the first time you install it.

## Tips for Best Experience

1. **Use headphones** for better audio quality
2. **Keep screen on** - Some devices may pause when the screen locks
3. **Adjust speed** - Try 1.2x to 1.5x for faster reading
4. **Choose clear voices** - Test different voices to find your favorite
5. **Split long books** - Very large files may take time to load

## Browser Compatibility

Works best on:
- ✅ iOS Safari (iPhone/iPad)
- ✅ Chrome (Android)
- ✅ Samsung Internet
- ✅ Desktop Chrome, Edge, Safari

Note: Text-to-speech quality varies by device and browser.

## Privacy

This app:
- ✅ Runs entirely on your device
- ✅ Does NOT upload your books anywhere
- ✅ Does NOT track you
- ✅ Stores data only in your browser's local storage

## Technical Details

Built with:
- HTML5
- CSS3 (with mobile-first responsive design)
- Vanilla JavaScript
- Web Speech API
- Service Workers for PWA functionality

## Troubleshooting

**App won't narrate:**
- Ensure your device volume is up
- Check that your browser supports Web Speech API
- Try a different browser

**Voice sounds robotic:**
- Some default voices are lower quality
- Try selecting a different voice
- iOS devices generally have better quality voices

**App won't install:**
- Make sure you're using a supported browser
- Some browsers require HTTPS for PWA installation

**Lost my progress:**
- If you cleared browser data, progress may be lost
- The app stores data in localStorage

## Development

To run locally:
1. Clone or download this repository
2. Serve the files with any local web server
3. Or simply open `index.html` in a browser

No build process or dependencies required!

## Future Enhancements

Potential features to add:
- Chapter detection and navigation
- Bookmarks
- Multiple book library
- Sleep timer
- Background audio playback
- Cloud sync across devices

## License

Free to use and modify for personal or commercial purposes.

## Credits

Created with Claude Code - An AI-powered development assistant.

---

Enjoy your audiobooks! 📖🎧
