import React, { useContext } from 'react';
import { SearchContext } from '../contexts/SearchContext';
import styles from '../styles/Home.module.scss';
import ProductCard from '../components/ProductCard';

export default function Home() {
  const { products, searchString } = useContext(SearchContext)

  return (
    <div className={styles.container}>
      {products.length ? (
        <div className={styles.productsContainer}>
          {products.map(product => {
            return <ProductCard product={product} key={product.id} />
          })}
        </div>
      ) : (
        searchString.length ? (
          <h1>Nenhum produto encontrado</h1>
        ) : (
          <h1>Faça uma busca para ver os produtos</h1>
        )
      )}
    </div>
  )
}
