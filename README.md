# Bioluminescent Detection AI - Frontend

A modern Next.js frontend for the Bioluminescent Detection AI system, built with TypeScript and Tailwind CSS.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn
- Backend API running on http://localhost:8000

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at http://localhost:3000

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── globals.css      # Global styles with Tailwind
│   │   ├── layout.tsx       # Root layout component
│   │   └── page.tsx         # Main page component
│   ├── components/          # React components
│   │   ├── PredictionTab.tsx
│   │   ├── WindSpeedConverterTab.tsx
│   │   ├── BulkPredictionTab.tsx
│   │   └── ModelInfoTab.tsx
│   ├── lib/                 # Utility libraries
│   │   ├── api.ts          # API client
│   │   └── utils.ts        # Utility functions
│   └── types/              # TypeScript type definitions
│       └── api.ts          # API types
├── package.json
├── tailwind.config.js      # Tailwind CSS configuration
├── next.config.js          # Next.js configuration
└── tsconfig.json           # TypeScript configuration
```

## 🎨 Features

### Core Functionality

- **AI Prediction**: Single prediction with comprehensive form validation
- **Wind Speed Converter**: Convert between 6 different wind speed units
- **Bulk Prediction**: Process multiple scenarios via CSV upload
- **Model Information**: View current model parameters and system status

### UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern Interface**: Clean, professional design with Tailwind CSS
- **Real-time Validation**: Form validation with helpful error messages
- **Loading States**: Smooth loading indicators and transitions
- **Toast Notifications**: User feedback for actions and errors

### Technical Features

- **TypeScript**: Full type safety throughout the application
- **React Hook Form**: Efficient form handling with validation
- **Axios**: HTTP client for API communication
- **Lucide Icons**: Beautiful, consistent iconography
- **Tailwind CSS**: Utility-first styling with custom components

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file in the root directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Tailwind CSS

The project uses Tailwind CSS with custom configuration:

- Custom color palette with primary and secondary colors
- Custom animations (fade-in, slide-up, pulse-slow)
- Responsive design utilities
- Custom component classes (btn-primary, card, input-field, etc.)

## 📱 Responsive Design

The application is fully responsive with:

- **Mobile-first approach**: Optimized for mobile devices
- **Tablet support**: Adaptive layouts for medium screens
- **Desktop optimization**: Enhanced features for large screens
- **Touch-friendly**: Large buttons and input fields for mobile

## 🚀 Deployment

### Development

```bash
npm run dev
```

### Production Build

```bash
npm run build
npm start
```

### Docker Deployment

```bash
# Build the Docker image
docker build -t bioluminescent-frontend .

# Run the container
docker run -p 3000:3000 bioluminescent-frontend
```

## 🧪 Testing

```bash
# Run type checking
npm run type-check

# Run linting
npm run lint
```

## 📦 Dependencies

### Core Dependencies

- **Next.js 14**: React framework with App Router
- **React 18**: UI library
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling framework

### UI/UX Dependencies

- **React Hook Form**: Form handling
- **React Hot Toast**: Toast notifications
- **Lucide React**: Icons
- **clsx & tailwind-merge**: Utility class management

### Development Dependencies

- **ESLint**: Code linting
- **PostCSS**: CSS processing
- **Autoprefixer**: CSS vendor prefixing

## 🔗 API Integration

The frontend communicates with the FastAPI backend through:

- **RESTful API**: Standard HTTP endpoints
- **Type-safe requests**: Full TypeScript integration
- **Error handling**: Comprehensive error management
- **Loading states**: User feedback during API calls

## 🎯 Key Components

### PredictionTab

- Comprehensive form for single predictions
- Real-time validation
- Beautiful results display with confidence intervals
- Performance metrics and warnings

### WindSpeedConverterTab

- Convert between 6 wind speed units
- Support for Beaufort scale
- Real-time conversion results

### BulkPredictionTab

- CSV file upload and processing
- Template download
- Batch results display
- Error handling for malformed data

### ModelInfoTab

- Current model parameters display
- System status information
- Input specification documentation
- Supported sensors list

## 🚀 Performance

- **Fast Loading**: Optimized bundle size
- **Efficient Rendering**: React optimization
- **Caching**: Next.js built-in caching
- **Code Splitting**: Automatic code splitting

## 🔒 Security

- **Input Validation**: Client and server-side validation
- **Type Safety**: TypeScript prevents runtime errors
- **Secure API Calls**: Proper error handling
- **XSS Protection**: React's built-in protection

## 📈 Future Enhancements

- **Real-time Data Visualization**: Charts and graphs
- **User Authentication**: Secure access control
- **Advanced Analytics**: Detailed performance metrics
- **Mobile App**: React Native companion app
- **Offline Support**: Service worker implementation

---

_Frontend Development - Updated: August 7, 2025_
_Status: ✅ READY FOR DEVELOPMENT_
