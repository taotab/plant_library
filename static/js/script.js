function toggleEdit(button) {
    const modal = button.closest('.modal-content');
    modal.querySelectorAll('.edit-field').forEach(el => el.classList.toggle('d-none'));
    modal.querySelector('.edit-actions').classList.toggle('d-none');
    modal.querySelector('.view-actions').classList.toggle('d-none');
}


// Function to auto dismiss alerts after a timeout

setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => alert.classList.remove('show'));
}, 5000);

function submitDeleteForm(id) {
    const confirmed = confirm("Are you sure you want to permanently delete this suggestion?");
    if (confirmed) {
        document.getElementById(`deleteForm${id}`).submit();
    }
}

function submitApproveForm(id) {
    const confirmed = confirm("Approve this suggestion and move it to the plant list?");
    if (confirmed) {
        document.getElementById(`approveForm${id}`).submit();
    }
}


// Function to handle toggle switch, approve and delete actions in dashboard
function showSection(section) {
    document.getElementById('pending-section').classList.add('d-none');
    document.getElementById('approved-section').classList.add('d-none');
    document.getElementById(section + '-section').classList.remove('d-none');
}

// Set initial view based on server-passed variable
// window.onload = function () {
//     const currentView = "{{ current_view }}";
//     showSection(currentView);

//     // Set the radio button accordingly
//     if (currentView === "approved") {
//         document.getElementById("approvedToggle").checked = true;
//     } else {
//         document.getElementById("pendingToggle").checked = true;
//     }
// };

window.onload = function () {
    const currentView = window.dashboardView || "pending";  // Fallback to "pending"
    showSection(currentView);

    if (currentView === "approved") {
        document.getElementById("approvedToggle").checked = true;
    } else {
        document.getElementById("pendingToggle").checked = true;
    }
};
