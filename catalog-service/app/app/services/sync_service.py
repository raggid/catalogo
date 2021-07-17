from app.services import product_service
from app.schemas.product_schemas import ProductWithSpecs
from app.schemas.tech_spec_schemas import TechSpec


def generate_spec(tech_spec: TechSpec):
    return {
        "name": tech_spec.spec_name,
        "value": tech_spec.spec_value,
        "unit": tech_spec.spec_unit
    }


def generate_search(product: ProductWithSpecs, tech_spec: TechSpec):
    return {
        "searchString": ' '.join([
            product.provider_code,
            product.provider_name,
            product.product_code,
            product.product_description,
            product.product_model,
            tech_spec.spec_name,
            tech_spec.spec_value
        ])
    }


def generate_product_payload(product: ProductWithSpecs):
    return {
        "internalCode": product.id,
        "masterCode": product.product_code,
        "provider": product.provider_name,
        "description": product.product_description,
        "techSpecs": [generate_spec(spec.tech_spec) for spec in product.product_specs],
        "searchContext": [generate_search(product, spec.tech_spec) for spec in product.product_specs]
    }


def sync_product(db, es, product_id: int):
    product = product_service.get_product_by_id(db, product_id)
    payload = generate_product_payload(product)
    res = es.index(index="product_index", id=product_id, body=payload)
    return {'result': res['result']}
