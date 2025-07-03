import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';

const vibrantBlue = '#2979ff';
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: vibrantBlue,
      contrastText: '#fff',
    },
    secondary: {
      main: '#00bcd4',
    },
    background: {
      default: '#181a20',
      paper: '#23263a',
    },
    text: {
      primary: '#fff',
      secondary: '#b0b8c1',
    },
    error: {
      main: '#ff5252',
    },
    warning: {
      main: '#ffb300',
    },
    info: {
      main: '#2196f3',
    },
    success: {
      main: '#4caf50',
    },
  },
  shape: {
    borderRadius: 12,
  },
  typography: {
    fontFamily: 'Inter, Segoe UI, Arial, sans-serif',
    fontWeightBold: 700,
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          minHeight: '100vh',
        },
      },
    },
  },
});

const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
const systemTheme = createTheme({ ...theme, palette: { ...theme.palette, mode: prefersDarkMode ? 'dark' : 'light' } });

ReactDOM.createRoot(document.getElementById('root')).render(
  <ThemeProvider theme={systemTheme}>
    <CssBaseline />
    <App />
  </ThemeProvider>
);
