import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export', // Enable static export
  trailingSlash: true,
  images: {
    unoptimized: true // Required for static export
  },
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
