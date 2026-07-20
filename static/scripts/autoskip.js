const elements = document.getElementsByTagName("audio");

for (let i = 0; i < elements.length; i++) {
    const current = elements.item(i);
    const next = elements.item(i+1);
    
    current.addEventListener("ended", function()
        {
            current.currentTime = 0;
            next.play();
        }
    );
}

