// app/index.tsx
import React from 'react';
import ChatScreen from '../components/ChatScreen';
import Head from 'expo-router/head';  

export default function Page() {
  return (
    <>
      <Head>
        <title>AI Billing Assistant</title>
      </Head>
      <ChatScreen />
    </>
  );
}

