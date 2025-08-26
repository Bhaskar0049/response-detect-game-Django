/**
 * Tailwind CSS configuration.
 *
 * This config is provided for completeness. The project uses the Tailwind CDN in
 * templates for simplicity; however, if you wish to build a custom bundle,
 * uncomment the `content` paths and run the Tailwind CLI to generate a
 * production CSS file.
 */
module.exports = {
  content: [
    './game/templates/**/*.html',
    './templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}