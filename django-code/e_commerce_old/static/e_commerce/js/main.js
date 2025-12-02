const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

document.addEventListener('DOMContentLoaded', function() {
    const mainProductImage = document.getElementById('mainProductImage');
    const thumbnailItems = document.querySelectorAll('.thumbnail-item');

    if (mainProductImage && thumbnailItems.length > 0) {
        thumbnailItems.forEach(thumbnail => {
            thumbnail.addEventListener('click', function() {
                // Remove 'active' class from all thumbnails
                thumbnailItems.forEach(item => item.classList.remove('active'));
                
                // Add 'active' class to the clicked thumbnail
                this.classList.add('active');
                
                // Change the main image src
                mainProductImage.src = this.dataset.largeImage;
            });
        });

        
        if (!document.querySelector('.thumbnail-item.active')) {
            thumbnailItems[0].classList.add('active');
            mainProductImage.src = thumbnailItems[0].dataset.largeImage;
        }
    }

    avatarElement = document.getElementById('avatar-initials-main')
    if (avatarElement) {
        const colorValue = avatarElement.dataset.color;

        // Assign the style using JavaScript (which is trusted by the nonce)
        if (colorValue) {
            avatarElement.style.backgroundColor = colorValue;
        }
    }

});


document.getElementById('flip-button').addEventListener('click', function() {
    this.classList.toggle('flipped');
});

