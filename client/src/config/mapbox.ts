// Map configuration for Leaflet (free alternative to Mapbox)
export const MAP_CONFIG = {
  // No API token needed for Leaflet with OpenStreetMap
  defaultCenter: {
    lng: Number(process.env.NEXT_PUBLIC_DEFAULT_LNG) || 77.5946,
    lat: Number(process.env.NEXT_PUBLIC_DEFAULT_LAT) || 12.9716,
  },
  defaultZoom: Number(process.env.NEXT_PUBLIC_DEFAULT_ZOOM) || 10,

  // Tile layer options
  tileLayer: {
    url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19,
  },

  // Alternative tile layers you can use:
  alternatives: {
    carto: {
      url: 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    },
    stamen: {
      url: 'https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}{r}.png',
      attribution:
        'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    },
  },
};
