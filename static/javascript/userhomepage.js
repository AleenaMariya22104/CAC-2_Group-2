
    function showProfile() {
      hideAllSections();
      document.getElementById('profileSection').style.display = 'block';
       fetch('/api/get_profile_details/')  // Replace with your actual API endpoint
      .then(response => response.json())
      .then(data => {
        // Update the profile details in the DOM
        document.getElementById('profileName').innerText = 'Welcome, ' + data.name;
        document.getElementById('profileEmail').innerText = 'YOUR EMAILID: ' + data.email;
        // Update other profile details as needed
      })
      .catch(error => console.error('Error fetching profile details:', error));
  }
    }

    function showUpdateProfile() {
      hideAllSections();
      document.getElementById('updateProfileSection').style.display = 'block';
    }

    function showElectricityBill() {
      hideAllSections();
      document.getElementById('electricityBillSection').style.display = 'block';
    }

    function showComplaintForm() {
      hideAllSections();
      document.getElementById('complaintFormSection').style.display = 'block';
    }

    function showPaymentForm() {
      hideAllSections();
      document.getElementById('paymentFormSection').style.display = 'block';
    }

    function hideAllSections() {
      document.getElementById('profileSection').style.display = 'none';
      document.getElementById('updateProfileSection').style.display = 'none';
      document.getElementById('electricityBillSection').style.display = 'none';
      document.getElementById('complaintFormSection').style.display = 'none';
      document.getElementById('paymentFormSection').style.display = 'none';
    }

    function updateProfile() {
      // Implement update profile functionality using JavaScript or make an API call
    }

    function registerComplaint() {
      // Implement complaint registration functionality using JavaScript or make an API call
    }

    function payBill() {
      // Implement bill payment functionality using JavaScript or make an API call
    }