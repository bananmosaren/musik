const elements = document.getElementsByTagName("audio");

const album = document.title;
for (let i = 0; i < elements.length; i++) {
    let current = elements.item(i);
    let next = elements.item(i+1);
    
    current.addEventListener("ended", function()
        {
            current.currentTime = 0;
            next.play();

            document.title = "–";
        }
    );
    
    current.addEventListener("play", function()
        {
            let title = current.title;
            document.title = title + " – " + album;
        }
    );
}

