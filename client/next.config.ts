import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  webpack: (config) => {
    // Fix for mapbox-gl
    config.module.rules.push({
      test: /\.mjs$/,
      include: /node_modules/,
      type: 'javascript/auto',
    });
    return config;
  },
  // Transpile mapbox-gl for Next.js
  transpilePackages: ['mapbox-gl'],
};

export default nextConfig;
