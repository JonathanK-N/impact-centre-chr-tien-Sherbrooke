import React, { useEffect } from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import useAuth from "./hooks/useAuth";
import { attachInterceptors } from "./services/api";
import ProtectedRoute from "./components/ProtectedRoute";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Departments from "./pages/Departments";
import Families from "./pages/Families";
import Events from "./pages/Events";
import Announcements from "./pages/Announcements";
import Media from "./pages/Media";
import Donations from "./pages/Donations";
import Profile from "./pages/Profile";
import Admin from "./pages/Admin";

export default function App() {
  const { user, accessToken, refreshToken, logout, loading } = useAuth();

  useEffect(() => {
    if (accessToken && refreshToken) {
      attachInterceptors(accessToken, refreshToken, logout);
    }
  }, [accessToken, refreshToken, logout]);

  if (loading) {
    return <div className="flex h-screen items-center justify-center text-slate-500">Chargement...</div>;
  }

  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to="/" replace /> : <Login />} />
      <Route path="/register" element={user ? <Navigate to="/" replace /> : <Register />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/departments"
        element={
          <ProtectedRoute>
            <Departments />
          </ProtectedRoute>
        }
      />
      <Route
        path="/families"
        element={
          <ProtectedRoute>
            <Families />
          </ProtectedRoute>
        }
      />
      <Route
        path="/events"
        element={
          <ProtectedRoute>
            <Events />
          </ProtectedRoute>
        }
      />
      <Route
        path="/announcements"
        element={
          <ProtectedRoute>
            <Announcements />
          </ProtectedRoute>
        }
      />
      <Route
        path="/media"
        element={
          <ProtectedRoute>
            <Media />
          </ProtectedRoute>
        }
      />
      <Route
        path="/donations"
        element={
          <ProtectedRoute>
            <Donations />
          </ProtectedRoute>
        }
      />
      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <Profile />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin"
        element={
          <ProtectedRoute roles={["admin"]}>
            <Admin />
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Navigate to={user ? "/" : "/login"} replace />} />
    </Routes>
  );
}
