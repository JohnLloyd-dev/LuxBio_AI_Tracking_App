/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  images: {
    domains: ["localhost"],
  },
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://83.229.67.244:8000/:path*",
      },
    ];
  },
};

module.exports = nextConfig;
