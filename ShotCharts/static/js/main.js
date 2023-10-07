





new Vue({
    el: "#app",
    data: {
        players: [], // Initializing empty array to store player data
        seasons: [],
        selectedSeason: '' // Initialize selected Season
    },
    methods: {
        loadPlayers: function () {
            fetch(`/api/players?season=${this.selectedSeason}`)
                .then(response => response.json())
                .then(data => {
                    this.players = data;
                })
                .catch(error => {
                    console.error("Error fetching player data: ", error);
                });
        }
    },
    watch: {
        // Watching for changes to the selectedSeason
        selectedSeason: function(newSeason, oldSeason) {
            // When selected season changes, call the loadPlayers method again
            this.loadPlayers();
        }
    },
    created: function() {
        this.selectedSeason = '2022-2023';
        // Call the loadPlayer method when component is created.
        this.loadPlayers();
    }

})