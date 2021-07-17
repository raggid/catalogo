import styles from './styles.module.scss';
import Image from 'next/image';
import Link from 'next/link';

type TechSpec = {
  name: string,
  value: string,
  unit: string
}

type Application = {
  name: string,
  types: string[]
}

type Product = {
  id: string
  code: string,
  provider: string,
  description: string,
  techSpecs: TechSpec[],
  applications: Application[]
}

type ProductCardProps = {
  product: Product
}

export default function ProductCard({ product }: ProductCardProps) {
  console.log(product)
  return (
    <div className={styles.container}>
      <Image src="/parts.png" width={192} height={192} objectFit="contain" />
      <div className={styles.details}>
        <h3>{product.description}</h3>
        <span>{product.code}</span>
        <span>{product.provider}</span>
      </div>
      <div className={styles.techSpecs}>
        <h3>Especificações Técnicas</h3>
        <div>
          {product.techSpecs.map(techSpec => {
            return (
              <div>
                <span>{techSpec.name}: </span>
                <span>{techSpec.value} </span>
                {techSpec.unit != '-' && <span>{techSpec.unit}</span>}
              </ div>
            )
          })}
        </div>
      </div>
      {/* <div className={styles.applications}>
        <h3>Aplicações</h3>
        <div>
          {product.applications.map(ap => {
            return (
              <div>
                <span>{ap.name}</span>
              </ div>
            )
          })}
        </div>
      </div> */}
    </div>
  )
}