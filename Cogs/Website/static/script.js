$(document).ready(function () {
            updateServerTypes();
            updateVersions();
            updateVanillaVersions();
            updateLogo();
        });

        // Function to update server types dropdown
        function updateServerTypes() {
            $.ajax({
                url: '/api/get_server_types',  // Update this URL with the route that returns server types
                type: 'GET',
                success: function (data) {
                    var serverTypeDropdown = $('#server-type');
                    serverTypeDropdown.empty();

                    // Populate server types dropdown
                    for (var i = 0; i < data.serverTypes.length; i++) {
                        serverTypeDropdown.append($('<option>', {
                            value: data.serverTypes[i],
                            text: data.serverTypes[i]
                        }));
                    }

                    // Update versions based on the selected server type
                    updateVersions();
                },
                error: function (error) {
                    console.error('Error fetching server types:', error);
                }
            });
        }

        // Function to update versions dropdown based on the selected server type
        function updateVersions() {
            var selectedServerType = $('#server-type').val();

            // Show or hide the release group container based on the selected server type
            var releaseGroupContainer = $('#release-group-container');
            releaseGroupContainer.toggle(selectedServerType === 'vanilla');

            // Fetch and populate release groups if the selected server type is 'vanilla'
            if (selectedServerType === 'vanilla') {
                $.ajax({
                    url: '/api/get_release_groups',  // Update this URL with the route that returns release groups
                    type: 'GET',
                    success: function (data) {
                        var releaseGroupDropdown = $('#release-group');
                        releaseGroupDropdown.empty();

                        // Populate release groups dropdown
                        for (var i = 0; i < data.releaseGroups.length; i++) {
                            releaseGroupDropdown.append($('<option>', {
                                value: data.releaseGroups[i],
                                text: data.releaseGroups[i]
                            }));
                        }
                    },
                    error: function (error) {
                        console.error('Error fetching release groups:', error);
                    }
                });
            }

            // Fetch and populate versions based on the selected server type
            $.ajax({
                url: '/api/get_server_versions/' + selectedServerType,  // Update this URL with the route that returns versions
                type: 'GET',
                success: function (data) {
                    var versionDropdown = $('#server-version');
                    versionDropdown.empty();

                    // Populate versions dropdown
                    for (var i = 0; i < data.versions.length; i++) {
                        versionDropdown.append($('<option>', {
                            value: data.versions[i],
                            text: data.versions[i]
                        }));
                    }
                },
                error: function (error) {
                    console.error('Error fetching server versions:', error);
                }
            });
        }

        function updateVanillaVersions() {
            console.log('Updating Vanilla Versions...');
            var selectedReleaseGroup = $('#release-group').val();
            console.log('Selected Release Group:', selectedReleaseGroup);

            $.ajax({
                url: '/api/get_versions/' + selectedReleaseGroup,  // Update this URL with the route that returns versions for a release group
                type: 'GET',
                success: function (data) {
                    var versionDropdown = $('#server-version');
                    versionDropdown.empty();

                    // Populate versions dropdown
                    for (var i = 0; i < data.versions.length; i++) {
                        versionDropdown.append($('<option>', {
                            value: data.versions[i],
                            text: data.versions[i]
                        }));
                    }
                },
                error: function (error) {
                    console.error('Error fetching versions:', error);
                }
        })};
        function updateLogo() {
            var serverType = document.getElementById("server-type").value;
            var logoElement = document.getElementById("server-logo");

            // Update the image source based on the selected server type
            switch (serverType) {
                case "vanilla":
                    logoElement.src = "/static/imgs/vanilla_logo.png"; // Replace with the actual path
                    break;
                case "spigot":
                    logoElement.src = "/static/imgs/spigot_logo.png"; // Replace with the actual path
                    break;
                case "paper":
                    logoElement.src = "/static/imgs/paper_logo.png"; // Replace with the actual path
                    break;
                default:
                    logoElement.src = "/static/imgs/vanilla_logo.png"; // Set a default image or leave it empty
                    break;
            }
        }

// Call the function on page load and when the server type changes
document.addEventListener("DOMContentLoaded", updateLogo);
document.getElementById("server-type").addEventListener("change", updateLogo);


    