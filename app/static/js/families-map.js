// Interactive Leaflet map for Familles d'Impact
document.addEventListener('DOMContentLoaded', () => {
    const mapElement = document.getElementById('impactMap');
    if (!mapElement || typeof L === 'undefined' || !Array.isArray(window.familiesData)) {
        return;
    }

    const locationStatus = document.getElementById('locationStatus');
    const distanceValue = document.getElementById('distanceValue');
    const travelSummary = document.getElementById('travelSummary');
    const directionsBtn = document.getElementById('directionsBtn');
    const contactBtn = document.getElementById('contactResponsible');
    const detailBtn = document.getElementById('familyDetailBtn');
    const familyList = document.getElementById('familyList');

    const defaultFamily = window.familiesData.find(f => f.latitude && f.longitude);
    const sherbrookeCenter = [45.4042, -71.8929];
    const map = L.map('impactMap', { scrollWheelZoom: true })
        .setView(defaultFamily ? [defaultFamily.latitude, defaultFamily.longitude] : sherbrookeCenter, 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
    }).addTo(map);

    const familyLayer = L.layerGroup().addTo(map);
    const userLayer = L.layerGroup().addTo(map);
    const markersById = {};

    window.familiesData.forEach(family => {
        if (!family.latitude || !family.longitude) {
            return;
        }
        const marker = L.marker([family.latitude, family.longitude]);
        marker.bindPopup(`<strong>${family.name}</strong><br><small>${family.address}</small>`);
        marker.on('click', () => selectFamily(family.id));
        marker.addTo(familyLayer);
        markersById[family.id] = marker;
    });

    let selectedFamily = null;
    let userLocation = null;
    let currentMode = 'driving';
    const selectedAddressEl = document.getElementById('selectedFamilyAddress');

    const travelModeLabels = {
        driving: 'en voiture',
        walking: 'à pied',
        transit: 'en bus',
        bicycling: 'à vélo'
    };

    const travelButtons = document.querySelectorAll('[data-travel-mode]');
    travelButtons.forEach(button => {
        button.addEventListener('click', () => {
            currentMode = button.dataset.travelMode;
            travelButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            updateDistanceDisplay();
        });
    });

    if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition((position) => {
            userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            userLayer.clearLayers();
            const userMarker = L.circleMarker([userLocation.lat, userLocation.lng], {
                radius: 10,
                color: '#00c2c7',
                fillColor: '#00c2c7',
                fillOpacity: 0.6
            }).addTo(userLayer);
            userMarker.bindPopup('Vous êtes ici').openPopup();
            map.flyTo([userLocation.lat, userLocation.lng], 13);
            locationStatus.textContent = 'Localisation activée';
            locationStatus.classList.remove('bg-light', 'text-dark');
            locationStatus.classList.add('bg-success', 'text-white');
            updateListDistances();
            focusNearestFamily();
        }, (error) => {
            console.warn('Geolocation error', error);
            locationStatus.textContent = 'Localisation refusée';
        }, { enableHighAccuracy: true });
    } else {
        locationStatus.textContent = 'Géolocalisation non disponible';
    }

    function selectFamily(familyId) {
        const family = window.familiesData.find(f => Number(f.id) === Number(familyId));
        if (!family) {
            return;
        }
        selectedFamily = family;
        document.getElementById('selectedFamilyName').textContent = family.name;
        selectedAddressEl.textContent = family.address || '';
        travelSummary.textContent = `Préparez votre itinéraire ${travelModeLabels[currentMode]}`;

        contactBtn.disabled = !(family.responsible && family.responsible.email);
        contactBtn.dataset.email = family.responsible && family.responsible.email ? family.responsible.email : '';
        detailBtn.disabled = !family.detail_url;
        detailBtn.dataset.url = family.detail_url || '';
        directionsBtn.disabled = !(family.latitude && family.longitude);

        if (family.responsible && family.responsible.name) {
            const pieces = [];
            if (family.address) {
                pieces.push(family.address);
            }
            pieces.push(`Référent : ${family.responsible.name}`);
            selectedAddressEl.textContent = pieces.join(' · ');
        }

        highlightListItem(familyId);

        if (family.latitude && family.longitude) {
            const marker = markersById[family.id];
            if (marker) {
                marker.openPopup();
                map.panTo(marker.getLatLng());
            }
        }

        updateDistanceDisplay();
    }

    function highlightListItem(familyId) {
        if (!familyList) return;
        familyList.querySelectorAll('.family-item').forEach(item => {
            item.classList.toggle('active', Number(item.dataset.familyId) === Number(familyId));
        });
    }

    function updateDistanceDisplay() {
        if (!selectedFamily) {
            distanceValue.textContent = '-';
            directionsBtn.disabled = true;
            return;
        }
        const distance = computeDistanceToSelected();
        if (distance !== null) {
            distanceValue.textContent = `${distance.toFixed(1)} km`;
            travelSummary.textContent = `Itinéraire ${travelModeLabels[currentMode]} vers ${selectedFamily.name}`;
            directionsBtn.disabled = false;
        } else {
            distanceValue.textContent = 'Activez votre position';
            travelSummary.textContent = 'Autorisez la localisation pour mesurer la distance.';
            directionsBtn.disabled = true;
        }
    }

    function computeDistanceToSelected() {
        if (!selectedFamily || !userLocation || !selectedFamily.latitude || !selectedFamily.longitude) {
            return null;
        }
        return haversine(userLocation.lat, userLocation.lng, selectedFamily.latitude, selectedFamily.longitude);
    }

    function haversine(lat1, lon1, lat2, lon2) {
        const R = 6371;
        const dLat = toRad(lat2 - lat1);
        const dLon = toRad(lon2 - lon1);
        const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }

    function toRad(value) {
        return value * Math.PI / 180;
    }

    function updateListDistances() {
        if (!familyList || !userLocation) {
            return;
        }
        familyList.querySelectorAll('.family-item').forEach(item => {
            const badge = item.querySelector('.family-distance');
            const familyId = Number(item.dataset.familyId);
            const family = window.familiesData.find(f => Number(f.id) === familyId);
            if (!badge || !family || !family.latitude || !family.longitude) {
                badge.textContent = '—';
                return;
            }
            const distance = haversine(userLocation.lat, userLocation.lng, family.latitude, family.longitude);
            badge.textContent = `${distance.toFixed(1)} km`;
        });
    }

    function focusNearestFamily() {
        if (!userLocation) {
            return;
        }
        const nearby = window.familiesData
            .filter(f => f.latitude && f.longitude)
            .map(f => ({
                ...f,
                distance: haversine(userLocation.lat, userLocation.lng, f.latitude, f.longitude)
            }))
            .sort((a, b) => a.distance - b.distance);
        if (nearby.length) {
            selectFamily(nearby[0].id);
        }
    }

    if (familyList) {
        familyList.querySelectorAll('.family-item').forEach(item => {
            item.addEventListener('click', () => {
                selectFamily(item.dataset.familyId);
            });
        });
    }

    directionsBtn.addEventListener('click', () => {
        if (!selectedFamily || !selectedFamily.latitude || !selectedFamily.longitude) {
            return;
        }
        const destination = `${selectedFamily.latitude},${selectedFamily.longitude}`;
        const params = new URLSearchParams({
            api: '1',
            destination,
            travelmode: currentMode
        });
        if (userLocation) {
            params.set('origin', `${userLocation.lat},${userLocation.lng}`);
        }
        const url = `https://www.google.com/maps/dir/?${params.toString()}`;
        window.open(url, '_blank');
    });

    contactBtn.addEventListener('click', () => {
        if (contactBtn.disabled || !contactBtn.dataset.email || !selectedFamily) {
            return;
        }
        const subject = encodeURIComponent(`Famille d'Impact - ${selectedFamily.name}`);
        window.location.href = `mailto:${contactBtn.dataset.email}?subject=${subject}`;
    });

    detailBtn.addEventListener('click', () => {
        if (detailBtn.disabled || !detailBtn.dataset.url) {
            return;
        }
        window.location.href = detailBtn.dataset.url;
    });

    if (!selectedFamily && window.familiesData.length) {
        selectFamily(window.familiesData[0].id);
    }
});
