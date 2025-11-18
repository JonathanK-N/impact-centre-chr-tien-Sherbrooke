import React from 'react';
import { View, StyleSheet } from 'react-native';
import { ActivityIndicator, Title } from 'react-native-paper';

const LoadingScreen = () => {
  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" color="#007bff" />
      <Title style={styles.title}>Impact Centre Sherbrooke</Title>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f8f9fa',
  },
  title: {
    marginTop: 20,
    color: '#007bff',
  },
});

export default LoadingScreen;