(function(){
  // Array to store the exact URLs
  let urlList = [];

  // Helper function: Check if the URL ends with "-512" before any query parameters.
  function isTargetUrl(url) {
    // Remove any query string portion to check the end.
    let baseUrl = url.split('?')[0];
    return baseUrl.endsWith("-512");
  }

  // Process a URL: if it meets our condition, add it to the list.
  function processUrl(url) {
    if (isTargetUrl(url)) {
      urlList.push(url);
      console.log("Added URL:", url);
      console.log("Current URL list:", urlList);
    }
  }

  // Adjust this selector if necessary to target your Slack profile picture element.
  const profilePicSelector = 'img.p-r_member_profile__avatar__img';
  const profilePicEl = document.querySelector(profilePicSelector);
  
  if (!profilePicEl) {
    console.log("Profile picture element not found. Please update the CSS selector.");
    return;
  }
  
  // Set up a MutationObserver to watch for changes in the 'src' attribute.
  const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
      if (mutation.type === 'attributes' && mutation.attributeName === 'src') {
        const newUrl = mutation.target.getAttribute('src');
        console.log("Profile picture updated. New URL:", newUrl);
        processUrl(newUrl);
      }
    });
  });

  observer.observe(profilePicEl, { attributes: true });
  console.log("Monitoring profile picture changes. Current URL list:", urlList);
})();
