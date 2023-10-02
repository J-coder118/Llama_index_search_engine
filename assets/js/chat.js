document.addEventListener('DOMContentLoaded', () => {
    const userChats = document.querySelectorAll('.user-chat');
    const chatMessages = document.querySelectorAll('.content-chat-message-user');

    userChats.forEach((userChat) => {
        userChat.addEventListener('click', () => {
            const selectedUsername = userChat.getAttribute('data-username');

            chatMessages.forEach((chatMessage) => {
                const messageUsername = chatMessage.getAttribute('data-username');

                if (messageUsername === selectedUsername) {
                    chatMessage.classList.add('active');
                } else {
                    chatMessage.classList.remove('active');
                }
            });

            userChats.forEach((chat) => {
                chat.classList.remove('active');
            });
            userChat.classList.add('active');
        });
    });

    // Activar el primer elemento user-chat inicialmente
    userChats[0].classList.add('active');
    chatMessages[0].classList.add('active');
});