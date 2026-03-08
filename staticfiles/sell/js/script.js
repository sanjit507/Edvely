  // ================= INFINITE TYPEWRITER EFFECT =================
    const textTarget = document.getElementById("typewriter");
    const wordToType = "Edvely";
    let charIndex = 0;
    let isDeleting = false;

    function infiniteTypeWriter() {
      // Get the current substring
      let currentText = wordToType.substring(0, charIndex);
      textTarget.textContent = currentText;

      // Default typing speed
      let typingSpeed = 150;

      if (!isDeleting) {
        // We are typing forward
        if (charIndex < wordToType.length) {
          charIndex++;
        } else {
          // Reached the end: pause, then start deleting
          isDeleting = true;
          typingSpeed = 2000; // Pause at full word for 2 seconds
        }
      } else {
        // We are deleting backward
        typingSpeed = 100; // Erase faster than typing
        if (charIndex > 0) {
          charIndex--;
        } else {
          // Reached the beginning: pause, then start typing again
          isDeleting = false;
          typingSpeed = 800; // Pause at blank text for 0.8 seconds
        }
      }

      // Loop the function recursively
      setTimeout(infiniteTypeWriter, typingSpeed);
    }
    
    // Start typing after a short delay on page load
    setTimeout(infiniteTypeWriter, 600);
