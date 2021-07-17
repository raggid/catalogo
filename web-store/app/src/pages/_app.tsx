import React, { useState } from 'react';
import '../styles/globals.scss';

import { Header } from '../components/Header';
import { SearchContext } from '../contexts/SearchContext';
import { api } from '../services/api';

function MyApp({ Component, pageProps }) {
  const [searchString, setSearchString] = useState('')
  const [products, setProducts] = useState([])

  function updateSearch(text: string) {
    setSearchString(text);
    searchProducts(text)
      .then(result => setProducts(result.products))
  }

  function updateProducts(newProducts) {
    setProducts(newProducts)
  }

  return (
    <SearchContext.Provider value={{ searchString, updateSearch, products, updateProducts }}>
      <div>
        <main>
          <Header />
          <Component {...pageProps} />
        </main>
      </div>
    </SearchContext.Provider>

  )
}

export const searchProducts = async (searchString: string) => {
  const { data } = await api.post('products/search-products', {
    text: `${searchString}`
  })

  const products = data.map(product => {
    return {
      id: product['internalCode'],
      code: product['masterCode'],
      provider: product['provider'],
      description: product['description'],
      techSpecs: product['techSpecs']
      // applications: product['applications']
    }
  })

  return {
    products
  }
}

export default MyApp
