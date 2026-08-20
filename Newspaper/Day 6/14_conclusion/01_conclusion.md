# 14.1 Conclusion

## Tổng kết

Survey cho thấy time-series preprocessing là một quy trình nhiều lớp: cleaning, transformation, feature processing, sensor fusion và compression. Mỗi lớp xử lý một failure mode khác nhau và có thể tác động tới cả chất lượng dữ liệu lẫn downstream model.

Empirical analysis trên AirQuality dùng pipeline có reserved-value handling, Grubbs/IQR, cubic spline, EM, feature selection và LSTM. Trong so sánh được paper minh họa, complete DAG đạt RMSE $0.32$, MAE $0.23$, MAPE $25.26\%$, so với $0.60$, $0.45$, $51.41\%$ của cấu hình preprocessing tối thiểu; paper báo cáo mức giảm lỗi xấp xỉ $46.66\%$, $48.88\%$ và $50.87\%$. Đây là bằng chứng trong context cụ thể, không phải bảng xếp hạng phổ quát.

## Kết luận phương pháp

Không tồn tại một preprocessing method tốt nhất cho mọi time series. Lựa chọn đúng phải dựa trên missing mechanism, distribution, temporal dependency, multivariate relation, resource constraint và downstream objective. Preprocessing mạnh hơn không tự động tốt hơn; nếu làm mất peak, future information hoặc provenance, nó có thể làm kết quả kém đáng tin.

## Limitations của diễn giải

Taxonomy rộng hơn phần empirical test; pipeline DAG thay nhiều bước nên không cô lập được tác động của từng component. UCI Appliances trong chương 13 là application transfer, không phải dataset của empirical paper. Những kết luận mới trên dataset đó cần thực nghiệm độc lập.

## Final principle

$$
\boxed{\text{Data characteristics}\rightarrow\text{Assumptions}\rightarrow\text{Preprocessing}\rightarrow\text{Validated downstream task}}
$$

Đó là logic cốt lõi để biến raw time series thành AI-ready data mà vẫn giữ được tính đúng đắn khoa học.