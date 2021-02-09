class BoggleGame{
    constructor(boardID, game_duration_secs = 60){
        this.game_duration_secs = game_duration_secs; // game length
        this.showTimer();

        this.score = 0;
        this.words = new Set();     // to avoid word duplication from user inputs. 
        this.board = $('#' + boardID);

        // for every 1000msec, do a tick.
        this.timer = setInterval(this.tick)

        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    }

    /* Show word in list of words */
    showWord(word){
        $(".words", this.board).append($("<li>", { text: word }));
    }

    /* show score in html */
    showScore(){
        $('.score', this.board).text(this.score);
    }

    /* show a status message */
    showMessage(msg, cls){
        $('.msg', this.board)
        .text(msg)
        .removeClass()
        .addClass(`msg ${cls}`);
    }

    /* handle user word submission. */
    async handleSubmit(e){
        // Prevent the page from refreshing.
        e.preventDefault();

        // Get the reference of word that the user has inputted. 
        const $word = $('.word', this.board);

        // Get the value of that word.
        let word = $word.val();

        // Get out if word does not exist.
        if (!word) return;

        // Check if the set 'words' already has the user word. 
        if (this.words.has(word)) {
            this.showMessage(`${word} already found`, 'err');
            return; 
        }
    
        // Send the word to the server to validate. 
        const response = await axios.get('/check-word', {params: {word: word}});
        if (response.data.result === 'not-word')
        {
            print('word is not a valid English word.');
        }
        else if (response.data.result === 'not-on-board')
        {
            print('not a valid word on this board.');
        }
        else
        {
            this.showWord(word);
            this.words.add(word);
            this.score += word.length;
            this.showScore();
        }
        $word.val('').focus();
    }

    /* Update timer in DOM */
    showTimer() {
        $('.timer', this.board).text(this.game_duration_secs);
    }

    /* Tick: process the second that is passing */
    async tick(){
        this.game_duration_secs -= 1;
        this.showTimer();

        if(this.game_duration_secs === 0){
            clearInterval(this.timer);
            await this.scoreGame();
        }
    }

    /* End of the game: show score and update message. */
    async scoreGame(){
        $('.add-word', this.board).hide();
        
        const res = await axios.post('/post-score', { score: this.score });
        if(res.data.newRecord){
            this.showMessage(`NEW RECORD: ${this.score}`, 'ok');
        } else {
            this.showMessage(`FINAL SCORE: ${this.score}`, 'ok');
        }
    }
}