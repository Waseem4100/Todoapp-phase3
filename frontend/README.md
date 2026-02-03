# Todo App Frontend

This is the frontend for the Todo Management System built with Next.js.

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Environment Variables

Create a `.env.local` file in the root of the frontend directory with the following:

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Building for Production

To build the application for production:

```bash
npm run build
```

## Deployment

This application is designed to be deployed on Vercel. To deploy:

1. Push your code to a GitHub repository
2. Connect your repository to [Vercel](https://vercel.com)
3. Vercel will automatically detect this is a Next.js app and build it

### Deploy to Vercel Button

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/your-repo-name)

## API Integration

The frontend connects to the backend API at the URL specified in the `NEXT_PUBLIC_API_BASE_URL` environment variable.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.