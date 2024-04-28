# API 文档
## 基础信息
- 基础URL: http://api.example.com
- 端口: 8000
- 版本: v1
## 1. 接收产品信息

- **URL:** `/submit_product`
- **方法:** `POST`
- **描述:** 接收和存储产品信息，包括产品名称、图片、Logo、品牌名称等。
- **请求体类型:** `multipart/form-data`
- **请求参数:**
  | 参数名        | 类型   | 描述                           | 是否必须 |
  | ------------- | ------ | ------------------------------ | -------- |
  | product_name  | string | 产品名称                       | 是       |
  | brand_name    | string | 品牌名称                       | 是       |
  | model         | string | 品牌车型                       | 否       |
  | description_1 | text   | 描述一                         | 否       |
  | description_2 | text   | 描述二                         | 否       |
  | description_3 | text   | 描述三                         | 否       |
  | image         | file   | 产品图片，支持jpg/jpeg/png/gif | 否       |
  | logo          | file   | 品牌Logo，支持jpg/jpeg/png/gif | 否       |

- **成功响应:**
  ```json
  {
    "id": "数据库中记录的ID",
    "product_name": "产品名称",
    "image_path": "保存的图片路径",
    "logo_path": "保存的Logo路径",
    "brand_name": "品牌名称",
    "model": "车型",
    "description_1": "描述一",
    "description_2": "描述二",
    "description_3": "描述三"
  }
- **错误响应:**
  - **400 Bad Request:**
    - **原因:** `Invalid file type.`
      - **内容:** 
        ```json
        {"message": "Invalid file type."}
        ```
    - **原因:** `Required fields are missing.`
      - **内容:** 
        ```json
        {"message": "Required fields are missing."}
        ```
## 2. 获取产品信息列表

- **URL:** `/get_products`
- **方法:** `GET`
- **描述:** 返回所有产品信息的列表。可以通过查询参数指定返回的产品数量。

- **请求参数:**

  | 参数名 | 类型 | 描述                          | 是否必须 |
  | ------ | ---- | ----------------------------- | -------- |
  | limit  | int  | 返回产品的数量，不指定则返回所有 | 否      |

- **成功响应:**

  ```json
  [
    {
      "id": "数据库中记录的ID",
      "product_name": "产品名称",
      "image_path": "图片路径",
      "logo_path": "Logo路径",
      "brand_name": "品牌名称",
      "model": "车型",
      "description_1": "描述一",
      "description_2": "描述二",
      "description_3": "描述三"
    },
    ...
  ]
## 3. 接收用户信息

### 接口详情

- **URL**: `/receive_info`
- **Method**: `POST`
- **Description**: 接收并存储用户的信息。Email 地址是必填项，其他信息为可选。

### 请求参数

请求体应为 `application/x-www-form-urlencoded` 或 `multipart/form-data` 类型，包括以下参数：

| 参数名            | 类型   | 描述             | 是否必须 |
|-------------------|--------|------------------|----------|
| Email             | string | 用户的邮箱地址   | 是       |
| Name              | string | 用户的姓名       | 否       |
| Country           | string | 用户的国家       | 否       |
| Client_Type       | string | 客户类型         | 否       |
| Interested_Vehicle | string | 感兴趣的车型     | 否       |
| Comment           | string | 附加评论         | 否       |

### 成功响应

- **Code**: `201 Created`
- **Content**:
  ```json
  {
    "success": true
  }
- **错误响应:**
  - **400 Bad Request:**
    - **内容:** 
      ```json
      {"message": "Email is required."}
      
## 4,获取用户信息接口

### 接口详情

- **URL**: `/get_info`
- **Method**: `GET`
- **Description**: 分页返回用户数据。可以通过查询参数指定页码和每页数量。

### 请求参数

此接口支持以下查询参数来控制分页：

| 参数名    | 类型 | 描述         | 是否必须 | 默认值 |
|-----------|------|--------------|----------|--------|
| page      | int  | 请求的页码   | 否       | 1      |
| per_page  | int  | 每页的记录数 | 否       | 10     |

### 成功响应

- **Code**: `200 OK`
- **Content**:
  ```json
  {
    "data": [
      {
        "user_id": "用户ID",
        "name": "用户名",
        "email": "用户邮箱",
        // 其他用户信息字段
      },
      // 更多用户数据
    ],
    "pagination": {
      "page": "当前页码",
      "per_page": "每页显示的记录数",
      "total": "总记录数",
      "pages": "总页数"
    }
  }
### 示例调用

请求第2页的数据，每页显示5条记录：

```http
GET /get_info?page=2&per_page=5
