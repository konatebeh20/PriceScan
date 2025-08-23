import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.pricescan.mobile',
  appName: 'PriceScan Mobile',
  webDir: 'dist/PriceScan-mobile/browser',
  server: {
    androidScheme: 'https'
  },
  plugins: {
    Camera: {
      permissions: ['camera', 'photos']
    },
    Storage: {
      permissions: ['storage']
    }
  }
};

export default config;
