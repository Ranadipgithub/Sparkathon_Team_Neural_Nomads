import { useEffect, useState } from "react"
import Title from "./Title"
import ProductItem from "./ProductItem"
import { productAPI } from "../utils/api"

const RelatedProducts = ({ category, subCategory, productId }) => {
  const [related, setRelated] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (productId) {
      loadRelatedProducts()
    }
  }, [productId])

  const loadRelatedProducts = async () => {
    try {
      setLoading(true)
      const response = await productAPI.getRelated(productId, 5)
      setRelated(response.products || [])
    } catch (error) {
      console.error("Error loading related products:", error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="my-24">
        <div className="text-center text-3xl py-2">
          <Title text1="RELATED" text2="PRODUCTS" />
        </div>
        <div className="flex justify-center py-10">
          <div className="text-gray-500">Loading related products...</div>
        </div>
      </div>
    )
  }

  if (related.length === 0) {
    return null
  }

  return (
    <div className="my-24">
      <div className="text-center text-3xl py-2">
        <Title text1="RELATED" text2="PRODUCTS" />
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 gap-y-6">
        {related.map((product, index) => (
          <ProductItem
            key={product._id || index}
            id={product._id}
            image={product.image}
            name={product.name}
            price={product.price}
          />
        ))}
      </div>
    </div>
  )
}

export default RelatedProducts
