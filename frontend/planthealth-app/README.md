# PlantHealth AI - Frontend

This is the React + Vite frontend for the PlantHealth AI project. It connects to the FastAPI backend to analyze plant images and detect diseases.

## Technologies

- React 19 + Vite
- Tailwind CSS v4
- Lucide React (Icons)
- Axios
- Capacitor (for Android/iOS builds)

## Getting Started

### Prerequisites

Ensure you have Node.js installed.

### Installation

1. Install the dependencies:
   ```bash
   npm install
   ```

2. Make sure you have a `.env` file in the root of the frontend project:
   ```env
   VITE_API_URL=http://localhost:8000
   ```
   *(Change the URL if your backend runs elsewhere)*

### Running Locally (Web)

Start the development server:
```bash
npm run dev
```

### Packaging as a Mobile App (APK)

This project uses Capacitor to generate native mobile apps.

1. **Build the web assets first:**
   ```bash
   npm run build
   ```
   *This creates the `dist` folder which Capacitor will package.*

2. **Add the Android platform:**
   ```bash
   npx cap add android
   ```

3. **Sync the project:**
   ```bash
   npx cap sync android
   ```

4. **Open in Android Studio to build the APK:**
   ```bash
   npx cap open android
   ```
   *From Android Studio, you can run the app on an emulator or build an APK (Build > Build Bundle(s) / APK(s) > Build APK(s)).*

*(For iOS, replace `android` with `ios` in the commands above, requiring macOS and Xcode).*
