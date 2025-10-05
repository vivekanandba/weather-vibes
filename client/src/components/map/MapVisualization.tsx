'use client';

import { Marker, Popup, CircleMarker } from 'react-leaflet';
import L from 'leaflet';
import { WhereResponse, WhenResponse, AdvisorResponse } from '../../types/api';

// Fix for default markers in Leaflet with Next.js
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

// @ts-expect-error - Leaflet icon fix
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl: markerIcon.src,
  iconRetinaUrl: markerIcon2x.src,
  shadowUrl: markerShadow.src,
});

interface MapVisualizationProps {
  whereData?: WhereResponse | null;
  whenData?: WhenResponse | null;
  advisorData?: AdvisorResponse | null;
}

export default function MapVisualization({ whereData, whenData, advisorData }: MapVisualizationProps) {
  // Ensure we're on the client side
  if (typeof window === 'undefined') {
    return null;
  }

  // Get score color based on normalized score (0-1)
  const getScoreColor = (score: number, maxScore: number, minScore: number) => {
    const normalized = (score - minScore) / (maxScore - minScore);
    if (normalized >= 0.8) return '#22c55e'; // Green - excellent
    if (normalized >= 0.6) return '#84cc16'; // Light green - good
    if (normalized >= 0.4) return '#eab308'; // Yellow - fair
    if (normalized >= 0.2) return '#f97316'; // Orange - poor
    return '#ef4444'; // Red - very poor
  };

  // Get month color based on score
  const getMonthColor = (score: number) => {
    if (score >= 80) return '#22c55e'; // Green - excellent
    if (score >= 70) return '#84cc16'; // Light green - good
    if (score >= 60) return '#eab308'; // Yellow - fair
    if (score >= 50) return '#f97316'; // Orange - poor
    return '#ef4444'; // Red - very poor
  };

  return (
    <>
      {/* Where Panel - Location Scores */}
      {whereData &&
        whereData.scores.map((location, index) => (
          <CircleMarker
            key={`where-${index}`}
            center={[location.lat, location.lon]}
            radius={8}
            pathOptions={{
              color: getScoreColor(location.score, whereData.max_score, whereData.min_score),
              fillColor: getScoreColor(location.score, whereData.max_score, whereData.min_score),
              fillOpacity: 0.7,
              weight: 2,
            }}
          >
            <Popup>
              <div style={{ minWidth: '200px' }}>
                <h3 style={{ margin: '0 0 8px 0', fontSize: '16px', fontWeight: 'bold' }}>
                  📍 {whereData.metadata.vibe_name}
                </h3>
                <p style={{ margin: '4px 0', fontSize: '14px' }}>
                  <strong>Score:</strong> {location.score.toFixed(1)}
                </p>
                <p style={{ margin: '4px 0', fontSize: '14px' }}>
                  <strong>Coordinates:</strong> {location.lat.toFixed(4)}, {location.lon.toFixed(4)}
                </p>
                <p style={{ margin: '4px 0', fontSize: '12px', color: '#666' }}>
                  Month: {whereData.metadata.center.lat ? 'Current' : 'Selected'}
                </p>
              </div>
            </Popup>
          </CircleMarker>
        ))}

      {/* When Panel - Best Location Marker */}
      {whenData && (
        <Marker position={[whenData.location.lat, whenData.location.lon]}>
          <Popup>
            <div style={{ minWidth: '200px' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '16px', fontWeight: 'bold' }}>
                📅 {whenData.metadata.vibe_name}
              </h3>
              <p style={{ margin: '4px 0', fontSize: '14px' }}>
                <strong>Best Month:</strong>{' '}
                {whenData.monthly_scores.find((m) => m.month === whenData.best_month)?.month_name} (
                {whenData.best_month})
              </p>
              <p style={{ margin: '4px 0', fontSize: '14px' }}>
                <strong>Worst Month:</strong>{' '}
                {whenData.monthly_scores.find((m) => m.month === whenData.worst_month)?.month_name} (
                {whenData.worst_month})
              </p>
              <p style={{ margin: '4px 0', fontSize: '14px' }}>
                <strong>Coordinates:</strong> {whenData.location.lat.toFixed(4)}, {whenData.location.lon.toFixed(4)}
              </p>
              <div style={{ marginTop: '8px' }}>
                <h4 style={{ margin: '0 0 4px 0', fontSize: '14px' }}>Monthly Scores:</h4>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '4px', fontSize: '12px' }}>
                  {whenData.monthly_scores.map((month) => (
                    <div
                      key={month.month}
                      style={{
                        padding: '2px 4px',
                        backgroundColor: getMonthColor(month.score),
                        color: 'white',
                        borderRadius: '3px',
                        textAlign: 'center',
                      }}
                    >
                      {month.month_name.substring(0, 3)}: {month.score.toFixed(0)}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </Popup>
        </Marker>
      )}

      {/* Advisor Panel - Location Marker */}
      {advisorData && (
        <Marker position={[advisorData.location.lat, advisorData.location.lon]}>
          <Popup>
            <div style={{ minWidth: '200px' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '16px', fontWeight: 'bold' }}>
                🤖 {advisorData.metadata.advisor_name}
              </h3>
              <p style={{ margin: '4px 0', fontSize: '14px' }}>
                <strong>Coordinates:</strong> {advisorData.location.lat.toFixed(4)},{' '}
                {advisorData.location.lon.toFixed(4)}
              </p>
              <div style={{ marginTop: '8px' }}>
                <h4 style={{ margin: '0 0 4px 0', fontSize: '14px' }}>Recommendations:</h4>
                {advisorData.recommendations.map((rec, index) => (
                  <div
                    key={index}
                    style={{
                      margin: '4px 0',
                      padding: '6px',
                      backgroundColor: '#f8f9fa',
                      borderRadius: '4px',
                      fontSize: '13px',
                    }}
                  >
                    <span style={{ fontSize: '16px', marginRight: '6px' }}>{rec.icon}</span>
                    <strong>{rec.item}</strong>
                    <p style={{ margin: '2px 0 0 0', color: '#666' }}>{rec.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </Popup>
        </Marker>
      )}
    </>
  );
}
