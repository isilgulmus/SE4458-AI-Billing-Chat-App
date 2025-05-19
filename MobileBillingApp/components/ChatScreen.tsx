"use client";

import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  FlatList,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  StyleSheet,
  ActivityIndicator
} from 'react-native';

import { db } from "./firebaseConfig";
import {
  collection,
  query,
  orderBy,
  onSnapshot
} from "firebase/firestore";

interface Message {
  id: string;
  from: 'user' | 'agent';
  text: string;
}

export default function ChatScreen() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [status, setStatus] = useState<'connecting' | 'open' | 'error'>('connecting');
  const [sending, setSending] = useState(false);
  const ws = useRef<WebSocket | null>(null);
  const didConnectRef = useRef(false);

  useEffect(() => {
    if (didConnectRef.current) return;
    didConnectRef.current = true;

    const socket = new WebSocket('wss://aiagentfr2025.azurewebsites.net/ws');
    ws.current = socket;

    socket.onopen = () => {
      setStatus('open');
      // Welcome message once
      setMessages([{ id: Date.now().toString(), from: 'agent', text: '👋 Welcome to the AI Billing Assistant!' }]);
    };

    socket.onmessage = ({ data }) => {
      if (sending) setSending(false);
      setMessages(prev => [...prev, { id: Date.now().toString(), from: 'agent', text: data }]);
    };

    socket.onerror = () => {
      setStatus('error');
      setSending(false);
      setMessages(prev => [...prev, { id: Date.now().toString(), from: 'agent', text: '❌ Connection error.' }]);
    };

    socket.onclose = () => {
      setStatus('error');
      setSending(false);
    };

    return () => {
      socket.close();
    };
  }, []);

  useEffect(() => {
  if (sending) {
    const timeout = setTimeout(() => {
      setSending(false);
    }, 10000);
    return () => clearTimeout(timeout);
  }
}, [sending]);

useEffect(() => {
  const q = query(
    collection(db, "chats", "session-1", "messages"),
    orderBy("timestamp", "asc")
  );

  const unsubscribe = onSnapshot(q, (querySnapshot) => {
    const newMessages = querySnapshot.docs.map(doc => ({
      id: doc.id,
      from: doc.data().from,
      text: doc.data().text
    }));
    setMessages(newMessages);
  });

  return () => unsubscribe();
}, []);


  const sendMessage = () => {
    if (input.trim() && ws.current?.readyState === WebSocket.OPEN) {
      setMessages(prev => [...prev, { id: Date.now().toString(), from: 'user', text: input }]);
      setSending(true);
      ws.current.send(input);
      setInput('');
    }
  };

  const renderItem = ({ item }: { item: Message }) => (
    <View style={[
      styles.bubble,
      item.from === 'user' ? styles.userBubble : styles.agentBubble
    ]}>
      <Text style={styles.bubbleText}>{item.text}</Text>
    </View>
  );

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      {status === 'connecting' && (
        <View style={styles.statusContainer}>
          <ActivityIndicator />
          <Text style={styles.statusText}>Connecting to server…</Text>
        </View>
      )}
      {status === 'error' && (
        <View style={styles.statusContainer}>
          <Text style={styles.errorText}>Connection error. Please try again.</Text>
        </View>
      )}

      <FlatList
        data={messages}
        renderItem={renderItem}
        keyExtractor={item => item.id}
        contentContainerStyle={styles.messagesContainer}
      />

      {sending && (
        <View style={styles.typingContainer}>
          <ActivityIndicator size="small" />
          <Text style={styles.typingText}>Agent is typing…</Text>
        </View>
      )}

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={input}
          onChangeText={setInput}
          placeholder="Type your message..."
          onSubmitEditing={sendMessage}
        />
        <TouchableOpacity style={styles.sendButton} onPress={sendMessage}>
          <Text style={styles.sendText}>Send</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 8,
    backgroundColor: '#f0f0f0'
  },
  statusText: { marginLeft: 8, fontSize: 14, color: '#333' },
  errorText: { fontSize: 14, color: 'red' },
  typingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 4
  },
  typingText: { marginLeft: 8, fontSize: 14, fontStyle: 'italic' },
  messagesContainer: { padding: 16 },
  bubble: { marginVertical: 4, padding: 12, borderRadius: 20, maxWidth: '80%' },
  userBubble: { backgroundColor: '#DCF8C6', alignSelf: 'flex-end' },
  agentBubble: { backgroundColor: '#ECECEC', alignSelf: 'flex-start' },
  bubbleText: { fontSize: 16 },
  inputContainer: { flexDirection: 'row', padding: 8, borderTopWidth: 1, borderColor: '#ddd' },
  input: { flex: 1, borderWidth: 1, borderColor: '#ddd', borderRadius: 20, paddingHorizontal: 16, paddingVertical: 8, fontSize: 16 },
  sendButton: { justifyContent: 'center', alignItems: 'center', paddingHorizontal: 16 },
  sendText: { fontSize: 16, color: '#007AFF' }
});
