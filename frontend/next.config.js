/** @type {import('next').NextConfig} */
const path = require('path')
const dotenv = require('dotenv')

// Load environment variables from root .env file
const envPath = path.resolve(__dirname, '../.env')
const envConfig = dotenv.config({ path: envPath })

if (envConfig.error) {
  console.warn('⚠️ Warning: Could not load .env file from:', envPath)
} else {
  console.log('✅ Loaded .env from:', envPath)
}

const nextConfig = {
  reactStrictMode: true,
  // Explicitly pass NEXT_PUBLIC_ variables to Next.js
  env: {
    NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  }
}

module.exports = nextConfig
