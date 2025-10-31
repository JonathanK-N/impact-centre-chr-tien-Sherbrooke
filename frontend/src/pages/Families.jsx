import React, { useCallback, useEffect, useMemo, useState } from "react";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

import DashboardLayout from "../layouts/DashboardLayout";
import useAuth from "../hooks/useAuth";
import api from "../services/api";

const defaultCenter = [45.4001, -71.8826];

const markerIcon = new L.Icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  shadowSize: [41, 41]
});

export default function Families() {
  const { user } = useAuth();
  const [families, setFamilies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedFamily, setSelectedFamily] = useState(null);
  const [search, setSearch] = useState("");
  const [form, setForm] = useState({
    name: "",
    description: "",
    address: "",
    city: "",
    postal_code: "",
    meeting_day: "",
    meeting_time: ""
  });

  const canCreate = ["admin", "family_lead"].includes(user.role);

  const loadFamilies = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await api.get("/families");
      setFamilies(data);
      if (data.length > 0) {
        setSelectedFamily(data[0]);
      }
    } catch (err) {
      setError(err.response?.data?.message || "Impossible de charger les familles");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadFamilies();
  }, [loadFamilies]);

  const handleSearch = async (event) => {
    event.preventDefault();
    try {
      const { data } = await api.post("/families/find", { postal_code: search });
      if (data.family) {
        setSelectedFamily(data.family);
      }
    } catch (err) {
      setError(err.response?.data?.message || "Aucune famille trouvée");
    }
  };

  const handleCreate = async (event) => {
    event.preventDefault();
    try {
      await api.post("/families", form);
      setForm({
        name: "",
        description: "",
        address: "",
        city: "",
        postal_code: "",
        meeting_day: "",
        meeting_time: ""
      });
      loadFamilies();
    } catch (err) {
      setError(err.response?.data?.message || "Impossible de créer la famille");
    }
  };

  const mapCenter = useMemo(() => {
    if (selectedFamily?.latitude && selectedFamily?.longitude) {
      return [selectedFamily.latitude, selectedFamily.longitude];
    }
    return defaultCenter;
  }, [selectedFamily]);

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-6">
        <header>
          <h1 className="text-2xl font-semibold text-primary-600">Familles d&apos;Impact</h1>
          <p className="mt-1 text-sm text-slate-500">
            Rejoignez un groupe de maison et découvrez ceux proches de chez vous.
          </p>
        </header>

        <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-700">Trouver une famille proche</h2>
          <form onSubmit={handleSearch} className="mt-4 flex flex-col gap-3 sm:flex-row">
            <input
              className="flex-1 rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              placeholder="Code postal"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
            <button
              type="submit"
              className="rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-500"
            >
              Rechercher
            </button>
          </form>
          {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
        </section>

        {canCreate && (
          <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-700">Créer une Famille d&apos;Impact</h2>
            <form onSubmit={handleCreate} className="mt-4 grid gap-4 md:grid-cols-2">
              {Object.entries(form).map(([key, value]) => (
                <div key={key} className="flex flex-col">
                  <label className="text-sm font-medium text-slate-600 capitalize">
                    {key.replace("_", " ")}
                  </label>
                  <input
                    value={value}
                    onChange={(event) =>
                      setForm((prev) => ({ ...prev, [key]: event.target.value }))
                    }
                    className="mt-1 rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  />
                </div>
              ))}
              <div className="md:col-span-2 flex justify-end">
                <button
                  type="submit"
                  className="rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-500"
                >
                  Enregistrer
                </button>
              </div>
            </form>
          </section>
        )}

        <section className="grid gap-6 lg:grid-cols-2">
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-700">Carte des familles</h2>
            <div className="mt-4 h-80 overflow-hidden rounded-lg">
              <MapContainer center={mapCenter} zoom={12} className="h-full w-full">
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                {families
                  .filter((family) => family.latitude && family.longitude)
                  .map((family) => (
                    <Marker
                      key={family.id}
                      position={[family.latitude, family.longitude]}
                      icon={markerIcon}
                      eventHandlers={{
                        click: () => setSelectedFamily(family)
                      }}
                    >
                      <Popup>
                        <p className="font-medium">{family.name}</p>
                        <p className="text-xs text-slate-500">{family.address}</p>
                        <p className="text-xs text-slate-500">
                          {family.meeting_day} {family.meeting_time}
                        </p>
                      </Popup>
                    </Marker>
                  ))}
              </MapContainer>
            </div>
          </div>
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-700">Familles</h2>
            {loading && <p className="mt-4 text-sm text-slate-500">Chargement...</p>}
            <ul className="mt-4 space-y-4">
              {families.map((family) => (
                <li
                  key={family.id}
                  className={`cursor-pointer rounded-lg border p-4 ${
                    selectedFamily?.id === family.id
                      ? "border-primary-300 bg-primary-50"
                      : "border-slate-200"
                  }`}
                  onClick={() => setSelectedFamily(family)}
                  role="presentation"
                >
                  <h3 className="font-medium text-slate-700">{family.name}</h3>
                  <p className="text-sm text-slate-500">{family.description}</p>
                  <p className="text-xs text-slate-400">
                    {family.meeting_day} {family.meeting_time}
                  </p>
                </li>
              ))}
            </ul>
          </div>
        </section>
      </div>
    </DashboardLayout>
  );
}
