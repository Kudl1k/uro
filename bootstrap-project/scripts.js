var dataList
var categories = new Set()
var letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
var numbers = ['1','2','3','4','5','6','7','8','9']
var brands = new Set()

function fetchdata(){
    let url = "https://dummyjson.com/products?limit=100";
    dataList = [];

    return fetch(url)
    .then(response => response.json())
    .then(data => {
        dataList = data.products.map((product, index) => {
            return {...product, placement: letters[index % 26] + numbers[index % 9]};
        });
        console.log(dataList);
        dataList.forEach(element => {
            categories.add(element.category)
            brands.add(element.brand)
        });
        fillData()
    })
    .catch(error => console.error('Error:', error));
}

function fillData(){
    fillTable()
    setupCategorySelector()
}

function setupCategorySelector(){
    let category_selector_content = '<option value="-1">Select Category</option>'
    let counter = 0;
    categories.forEach(element => {
        category_selector_content += `<option value="${counter}">${element}</option>`
        counter++
    });
    document.getElementById('category-combobox').innerHTML = category_selector_content
}

function fillTable(){
    let table_content_div = document.getElementById('table-content')

    let table_content = ""

    dataList.forEach(element => {
        table_content += `<tr onclick="location.href='edit_product.html?id=${element.id}'" style="cursor: pointer;">
        <th scope="row">${element.id}</th>
        <td>${element.title}</td>
        <td>${element.price}</td>
        <td>${element.stock}</td>
        <td>${element.brand}</td>
        <td>${element.category}</td>
        <td>${element.placement}</td>
      </tr>`
    });
    table_content_div.innerHTML = table_content
}

fetchdata().then(() => {
    const brandsel = document.getElementById('brand-select');
    brands.forEach(brand => {
        const option = document.createElement('option');
        option.value = brand;
        option.text = brand;
        brandsel.appendChild(option);
    });
    const categorysel = document.getElementById('category-select')
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.text = category;
        categorysel.appendChild(option);
    });
    const lettersel = document.getElementById('letter-select');
    letters.forEach(letter =>{
        const option = document.createElement('option')
        option.value = letter
        option.text = letter
        lettersel.appendChild(option)
    })
    
    const numbersel = document.getElementById('number-select');
    numbers.forEach(number =>{
        const option = document.createElement('option')
        option.value = number
        option.text = number
        numbersel.appendChild(option)
    })
});

document.getElementById('edit-photos-button').addEventListener('click', () => {
    window.alert('insert photos')  
})
document.getElementById('add-product-button').addEventListener('click', () => {
    window.alert('product added')  
})



