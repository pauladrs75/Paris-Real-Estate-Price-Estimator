$(document).ready(function() {
    $("#estimateForm").submit(function(event) {
        event.preventDefault();
        
        var formData = new FormData(this);

        // Translate type_of_good value
        var typeOfGood = formData.get('type_of_good');
        if (typeOfGood === 'Apartment') {
            formData.set('type_of_good', 'Appartement');
        } else if (typeOfGood === 'House') {
            formData.set('type_of_good', 'Maison');
        }

        // Rename form fields if necessary
        formData.set('adresse_numero', formData.get('street_number'));
        formData.set('adresse_nom_voie', formData.get('street_name'));
        formData.set('code_postal', formData.get('district'));
        formData.set('surface_reelle_bati', formData.get('sq_meters'));
        formData.set('nombre_pieces_principales', formData.get('main_rooms'));
        formData.set('type_local', formData.get('type_of_good'));
        formData.set('floor_level', formData.get('floor'));
        
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/predict_home_price",
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response && response.estimated_price) {
                    $("#uiEstimatedPrice").text(response.estimated_price + " €");
                } else {
                    console.error("Invalid response:", response);
                    $("#uiEstimatedPrice").text("Error: Invalid response from server");
                }
            },
            error: function(xhr, status, error) {
                console.error("Error details:", {
                    status: status,
                    error: error,
                    responseText: xhr.responseText
                });
                $("#uiEstimatedPrice").text("Error estimating price. Please check the console for details.");
            }
        });
    });
});
