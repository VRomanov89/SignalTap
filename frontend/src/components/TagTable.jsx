console.log('TagTable loaded!');
import React from 'react';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Switch from '@mui/material/Switch';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormGroup from '@mui/material/FormGroup';
import Checkbox from '@mui/material/Checkbox';

const TAG_TYPES = ['BOOL', 'INT', 'DINT', 'REAL', 'TIMER', 'STRING'];

export default function TagTable({ tags }) {
  const [filter, setFilter] = React.useState('');
  const [hideUnreadable, setHideUnreadable] = React.useState(false);
  const [typeFilters, setTypeFilters] = React.useState(TAG_TYPES.reduce((acc, t) => ({ ...acc, [t]: true }), {}));

  const handleTypeFilterChange = (type) => {
    setTypeFilters(prev => ({ ...prev, [type]: !prev[type] }));
  };

  const filteredTags = Array.isArray(tags)
    ? tags.filter(tag => {
        const matchesText = (
          tag.name.toLowerCase().includes(filter.toLowerCase()) ||
          (tag.type || '').toLowerCase().includes(filter.toLowerCase()) ||
          (tag.value !== undefined && String(tag.value).toLowerCase().includes(filter.toLowerCase()))
        );
        const notUnreadable = !hideUnreadable || tag.value !== 'Unreadable';
        const matchesType = tag.type && typeFilters[tag.type.toUpperCase()];
        return matchesText && notUnreadable && matchesType;
      })
    : [];

  if (!Array.isArray(tags) || tags.length === 0) {
    return (
      <Paper elevation={2} sx={{ p: 4, textAlign: 'center', color: 'text.secondary', minHeight: 120, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', bgcolor: 'background.paper' }}>
        <svg width="40" height="40" fill="none" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#e0e7ef"/><path d="M10 10h4v4h-4z" fill="#2563eb"/><path d="M12 6v2m0 8v2m6-6h-2M8 12H6" stroke="#2563eb" strokeWidth="1.5" strokeLinecap="round"/></svg>
        <Typography variant="body1" sx={{ mt: 2 }}>No tags found. Try scanning a PLC.</Typography>
      </Paper>
    );
  }
  return (
    <Paper elevation={2} sx={{ p: 3, mb: 4, bgcolor: 'background.paper', color: 'text.primary' }}>
      <Typography variant="h6" sx={{ mb: 2, fontWeight: 700 }}>PLC Tag Table</Typography>
      <FormControlLabel
        control={<Switch checked={hideUnreadable} onChange={e => setHideUnreadable(e.target.checked)} color="primary" />}
        label={<span>Hide Unreadable Tags</span>}
        sx={{ mb: 2, ml: 0 }}
      />
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mb: 2 }}>
        <Box>
          <input
            id="tag-filter"
            type="text"
            placeholder="Filter tags by name, type, or value..."
            value={filter}
            onChange={e => setFilter(e.target.value)}
            autoComplete="off"
            style={{ width: '100%', padding: '12px', borderRadius: 6, border: '1.5px solid #444', fontSize: '1.1rem', background: 'inherit', color: 'inherit' }}
          />
        </Box>
        <FormGroup row sx={{ flexWrap: 'wrap', gap: 2, mt: 1 }}>
          {TAG_TYPES.map(type => (
            <FormControlLabel
              key={type}
              control={<Checkbox checked={typeFilters[type]} onChange={() => handleTypeFilterChange(type)} color="primary" />}
              label={type}
              sx={{ color: 'text.primary', mr: 2 }}
            />
          ))}
        </FormGroup>
      </Box>
      <TableContainer sx={{ bgcolor: 'background.paper' }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: 700, color: 'text.secondary', bgcolor: 'background.paper' }}>Name</TableCell>
              <TableCell sx={{ fontWeight: 700, color: 'text.secondary', bgcolor: 'background.paper' }}>Type</TableCell>
              <TableCell sx={{ fontWeight: 700, color: 'text.secondary', bgcolor: 'background.paper' }}>Value</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredTags.map((tag, i) => (
              <TableRow key={i}>
                <TableCell>{tag.name}</TableCell>
                <TableCell>{tag.type}</TableCell>
                <TableCell>{tag.value}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
} 