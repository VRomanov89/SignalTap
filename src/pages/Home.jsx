import React, { useState } from 'react';
import Layout from '../components/Layout';
import PLCConnectForm from '../components/PLCConnectForm';
import TagTable from '../components/TagTable';
import Dashboard from '../components/Dashboard';

const Home = () => {
  const [tags, setTags] = useState([]);
  const [selectedTags, setSelectedTags] = useState([]);

  const handleScanComplete = (scannedTags) => {
    setTags(scannedTags);
  };

  return (
    <Layout>
      <div className="flex flex-col gap-8 w-full max-w-3xl">
        <PLCConnectForm onScanComplete={handleScanComplete} />
        <TagTable tags={tags} onSelectTag={() => {}} />
        <Dashboard tagValues={[]} />
      </div>
    </Layout>
  );
};

export default Home; 