import React, { useState, useEffect } from 'react';
import Layout from './components/Layout';
import PLCConnectForm from './components/PLCConnectForm';
import TagTable from './components/TagTable';
import Dashboard from './components/Dashboard';
import { scanTags, readTags } from './services/api';

export default function App() {
  const [ip, setIp] = useState('');
  const [slot, setSlot] = useState('0');
  const [tags, setTags] = useState([]);
  const [tagValues, setTagValues] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleScan = async () => {
    setLoading(true);
    setError(null);
    try {
      const slotNumber = parseInt(slot) || 0;
      const tags = await scanTags(ip.trim(), slotNumber);
      setTags(tags);
    } catch (err) {
      setError(err.message || 'Failed to connect to PLC. Please check the IP and try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let interval;
    if (ip && tags.length > 0) {
      const fetchTagValues = async () => {
        try {
          const tagNames = tags.map(tag => tag.name);
          const values = await readTags(ip, tagNames);
          setTagValues(values);
        } catch (err) {
          // Optionally handle error
        }
      };
      fetchTagValues(); // Initial fetch
      interval = setInterval(fetchTagValues, 2000); // Poll every 2 seconds
    } else {
      setTagValues([]);
    }
    return () => interval && clearInterval(interval);
  }, [ip, tags]);

  // Merge tags and tagValues for the table
  const tagsWithValues = tags.map(tag => {
    const valueObj = tagValues.find(v => v.name === tag.name);
    return {
      ...tag,
      value: valueObj ? valueObj.value : ''
    };
  });

  return (
    <Layout>
      <PLCConnectForm
        ip={ip}
        slot={slot}
        onIpChange={setIp}
        onSlotChange={setSlot}
        onScan={handleScan}
        loading={loading}
        error={error}
      />
      <TagTable tags={tagsWithValues} />
    </Layout>
  );
}
