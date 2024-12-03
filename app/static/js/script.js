document.getElementById("search-btn").addEventListener("click", async function() {
    const selectedBrands = Array.from(document.querySelectorAll('input[name="brand"]:checked')).map(input => input.value);
    const selectedCategories = Array.from(document.querySelectorAll('input[name="category"]:checked')).map(input => input.value);
    const selectedFlavours = Array.from(document.querySelectorAll('input[name="flavour"]:checked')).map(input => input.value);
    const selectedStrength = Array.from(document.querySelectorAll('input[name="strength"]:checked')).map(input => input.value);

    let queryParams = [];

    if (selectedBrands.length > 0) {
        selectedBrands.forEach(brandId => {
            queryParams.push(`brand_id=${brandId}`);
        });
    }

    if (selectedCategories.length > 0) {
        selectedCategories.forEach(categoryId => {
            queryParams.push(`category_id=${categoryId}`);
        });
    }

    if (selectedFlavours.length > 0) {
        selectedFlavours.forEach(flavourId => {
            queryParams.push(`flavour_id=${flavourId}`);
        });
    }

    if (selectedStrength.length > 0) {
        selectedStrength.forEach(strength => {
            queryParams.push(`strength=${strength}`);
        });
    }

    const url = `/api/tobacco?${queryParams.join('&')}`;

    try {
        const response = await fetch(url);
        const tobaccos = await response.json();

        const listContainer = document.querySelector('.list');

        listContainer.innerHTML = '';

        tobaccos.forEach(item => {

            const listItem = document.createElement('div');
            listItem.classList.add('list-item');

            const link = document.createElement('a');
            link.href = `/api/tobacco/${item.id}`;

            const img = document.createElement('img');
            img.src = `/static/images/tobacco/${item.id}.png`;

            const brandLabel = document.getElementById(`label_${item.brand_id}`);
            const brandName = document.createElement('div');
            brandName.textContent = brandLabel.textContent;

            const tobaccoName = document.createElement('div');
            tobaccoName.textContent = item.name;

            link.appendChild(img);
            link.appendChild(brandName);
            link.appendChild(tobaccoName);

            listItem.appendChild(link);

            listContainer.appendChild(listItem);
        });

    } catch (error) {
        console.error("Error fetching tobaccos:", error);
    }
});
