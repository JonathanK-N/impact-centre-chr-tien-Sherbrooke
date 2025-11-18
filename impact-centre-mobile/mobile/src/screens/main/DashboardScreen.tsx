import React from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  RefreshControl,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Button,
  Avatar,
  List,
  Divider,
} from 'react-native-paper';
import { useQuery } from 'react-query';

import { useAuth } from '../../store/AuthContext';
import { eventService, departmentService } from '../../services/api';

const DashboardScreen = () => {
  const { user } = useAuth();

  const { data: upcomingEvents, isLoading: eventsLoading, refetch: refetchEvents } = useQuery(
    'upcomingEvents',
    () => eventService.getAll({
      startDate: new Date().toISOString(),
      endDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString()
    })
  );

  const { data: departments, isLoading: departmentsLoading, refetch: refetchDepartments } = useQuery(
    'departments',
    departmentService.getAll
  );

  const handleRefresh = () => {
    refetchEvents();
    refetchDepartments();
  };

  const isRefreshing = eventsLoading || departmentsLoading;

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={isRefreshing} onRefresh={handleRefresh} />
      }
    >
      {/* Welcome Card */}
      <Card style={styles.welcomeCard}>
        <Card.Content style={styles.welcomeContent}>
          <Avatar.Text
            size={60}
            label={`${user?.firstName?.[0]}${user?.lastName?.[0]}`}
            style={styles.avatar}
          />
          <View style={styles.welcomeText}>
            <Title>Bonjour {user?.firstName}!</Title>
            <Paragraph>Bienvenue dans votre espace Impact Centre</Paragraph>
          </View>
        </Card.Content>
      </Card>

      {/* Quick Actions */}
      <Card style={styles.card}>
        <Card.Content>
          <Title>Actions rapides</Title>
          <View style={styles.quickActions}>
            <Button
              mode="contained"
              icon="calendar"
              style={styles.actionButton}
              onPress={() => {}}
            >
              Événements
            </Button>
            <Button
              mode="contained"
              icon="people"
              style={styles.actionButton}
              onPress={() => {}}
            >
              Départements
            </Button>
          </View>
        </Card.Content>
      </Card>

      {/* Upcoming Events */}
      <Card style={styles.card}>
        <Card.Content>
          <Title>Événements à venir</Title>
          {upcomingEvents?.events?.length > 0 ? (
            upcomingEvents.events.slice(0, 3).map((event: any) => (
              <View key={event._id}>
                <List.Item
                  title={event.title}
                  description={new Date(event.startDate).toLocaleDateString('fr-FR')}
                  left={(props) => <List.Icon {...props} icon="calendar" />}
                  onPress={() => {}}
                />
                <Divider />
              </View>
            ))
          ) : (
            <Paragraph>Aucun événement à venir</Paragraph>
          )}
          <Button mode="text" onPress={() => {}}>
            Voir tous les événements
          </Button>
        </Card.Content>
      </Card>

      {/* My Departments */}
      <Card style={styles.card}>
        <Card.Content>
          <Title>Mes départements</Title>
          {user?.departments?.length > 0 ? (
            user.departments.slice(0, 3).map((dept: any) => (
              <List.Item
                key={dept.departmentId}
                title={dept.name || 'Département'}
                description="Membre actif"
                left={(props) => <List.Icon {...props} icon="account-group" />}
                onPress={() => {}}
              />
            ))
          ) : (
            <Paragraph>Vous n'êtes membre d'aucun département</Paragraph>
          )}
          <Button mode="text" onPress={() => {}}>
            Voir tous les départements
          </Button>
        </Card.Content>
      </Card>

      {/* Statistics */}
      <Card style={styles.card}>
        <Card.Content>
          <Title>Statistiques</Title>
          <View style={styles.statsContainer}>
            <View style={styles.statItem}>
              <Title>{user?.departments?.length || 0}</Title>
              <Paragraph>Départements</Paragraph>
            </View>
            <View style={styles.statItem}>
              <Title>{user?.families?.length || 0}</Title>
              <Paragraph>Familles</Paragraph>
            </View>
            <View style={styles.statItem}>
              <Title>0</Title>
              <Paragraph>Événements</Paragraph>
            </View>
          </View>
        </Card.Content>
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  welcomeCard: {
    margin: 16,
    marginBottom: 8,
  },
  welcomeContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  avatar: {
    marginRight: 16,
  },
  welcomeText: {
    flex: 1,
  },
  card: {
    margin: 16,
    marginTop: 8,
  },
  quickActions: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 16,
  },
  actionButton: {
    flex: 1,
    marginHorizontal: 8,
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 16,
  },
  statItem: {
    alignItems: 'center',
  },
});

export default DashboardScreen;