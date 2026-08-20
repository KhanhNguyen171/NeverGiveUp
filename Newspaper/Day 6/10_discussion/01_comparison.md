# 10.1 So sánh theo tiêu chí

| Nhóm | Tận dụng temporal context | Chi phí | Điểm mạnh | Rủi ro |
|---|---|---:|---|---|
| Simple/statistical cleaning | thấp đến vừa | thấp | dễ audit, nhanh | làm phẳng hoặc lệch distribution |
| Interpolation | vừa | thấp-vừa | giữ continuity | sai khi gap dài/peak |
| Model-based imputation | cao | cao | học dependency | phụ thuộc model/assumption |
| Feature selection | gián tiếp | thấp-cao | giảm dimension | bỏ nhầm interaction |
| Sensor fusion | cao nếu aligned | vừa-cao | thêm context | misalignment, missing lan truyền |
| Compression | không trực tiếp | thấp-cao | giảm bandwidth/storage | information loss nếu lossy |

## Interpretation

Không có trục “accuracy” đơn lẻ cho các nhóm vì chúng giải quyết các failure mode khác nhau. Một pipeline tốt phải chọn theo pattern dữ liệu và chi phí hệ thống, sau đó đo downstream task.