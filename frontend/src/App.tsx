/**
 * Main App component with routing
 */
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Dashboard } from './pages/Dashboard';
import { Leaderboard } from './pages/Leaderboard';
import { Profile } from './pages/Profile';
import { socketService } from './lib/socket';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  useEffect(() => {
    // Connect to Socket.IO on mount
    socketService.connect();

    // Set up event listeners
    socketService.on('level_up', (data) => {
      console.log('Level up!', data);
      // TODO: Show notification
      queryClient.invalidateQueries({ queryKey: ['user'] });
    });

    socketService.on('tool_unlocked', (data) => {
      console.log('Tool unlocked!', data);
      // TODO: Show notification
      queryClient.invalidateQueries({ queryKey: ['tools'] });
    });

    return () => {
      socketService.disconnect();
    };
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-900 text-white">
          <Navbar />
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
            <Route path="/profile/:discordId" element={<Profile />} />
          </Routes>
        </div>
      </BrowserRouter>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

export default App;

