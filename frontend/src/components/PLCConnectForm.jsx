import React from 'react';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Alert from '@mui/material/Alert';

export default function PLCConnectForm({ ip, slot, onIpChange, onSlotChange, onScan, loading, error }) {
  return (
    <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
      <Box component="form" onSubmit={e => { e.preventDefault(); onScan(); }} sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', alignItems: 'center' }}>
        <TextField
          id="plc-ip"
          label="PLC IP Address"
          type="text"
          value={ip}
          onChange={e => onIpChange(e.target.value)}
          autoComplete="off"
          required
          sx={{ flex: 2, minWidth: 220 }}
        />
        <TextField
          id="plc-slot"
          label="Slot"
          type="number"
          min={0}
          value={slot}
          onChange={e => onSlotChange(e.target.value)}
          autoComplete="off"
          required
          sx={{ flex: 1, minWidth: 100 }}
        />
        <Button type="submit" variant="contained" color="primary" disabled={loading} sx={{ height: 56, minWidth: 160, fontWeight: 700 }}>
          {loading ? 'Scanning...' : 'Scan PLC Tags'}
        </Button>
      </Box>
      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
    </Paper>
  );
} 