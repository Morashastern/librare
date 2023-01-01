const displatbooks = async () => {
    const res = await axios.get(MY_SERVER + "/Books/")
    Books_display.innerHTML = `
    <table class="tabledisplay" id="booksDisplay">
    <thread>
        <tr style="color: darkolivegreen;border: 1cm;">
            <th scope="col">Book name</th>
            <th scope="col">Author</th>
            <th scope="col">Year Published</th>
            <th scope="col">Book Type</th>
            <th scope="col">Delete</th>
            <th scope="col">update</th>

        </tr>
    </thread>`
    Books_display2.innerHTML += res.data.map(book => `
    </tr>
    <td>${book.Name_book}</td>
    <td>${book.Author}</td>
    <td>${book.YearPublished}</td>
    <td>${book.Book_Type}</td>
    <td>${book.Name_book}</td>


    </table>`)
    console.log(res.data)
}
