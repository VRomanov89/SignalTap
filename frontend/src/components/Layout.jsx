import React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';

function SignalTapLogo({ size = 32 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="4" y="10" width="24" height="12" rx="6" fill="#2979ff" />
      <rect x="10" y="15" width="12" height="2" rx="1" fill="#fff" />
      <circle cx="24" cy="16" r="2" fill="#fff" />
      <circle cx="8" cy="16" r="2" fill="#fff" />
    </svg>
  );
}

export default function Layout({ children }) {
  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      <AppBar position="static" color="default" elevation={2} sx={{ bgcolor: 'background.paper', borderBottom: '1px solid #232936' }}>
        <Toolbar sx={{ justifyContent: 'center' }}>
          <SignalTapLogo size={32} />
          <Typography variant="h5" component="div" sx={{ fontWeight: 700, letterSpacing: 1, color: 'text.primary', ml: 2 }}>
            SignalTap PLC Tag Scanner
          </Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="md" sx={{ py: 4 }}>
        {children}
      </Container>
      <Box component="footer" sx={{ mt: 6, py: 3, bgcolor: 'background.paper', borderTop: '1px solid #232936', textAlign: 'center' }}>
        <Typography variant="body2" sx={{ color: 'text.secondary', mb: 1 }}>
          &copy; {new Date().getFullYear()} SignalTap &mdash; Built by 
          <a href="https://www.linkedin.com/in/vladromanov/" target="_blank" rel="noopener noreferrer" style={{ color: '#2979ff', textDecoration: 'none', marginLeft: 4, marginRight: 4 }}>Vladimir Romanov</a>
          | 
          <a href="https://joltek.com" target="_blank" rel="noopener noreferrer" style={{ color: '#2979ff', textDecoration: 'none', marginLeft: 4 }}>Joltek</a>
        </Typography>
      </Box>
    </Box>
  );
} 