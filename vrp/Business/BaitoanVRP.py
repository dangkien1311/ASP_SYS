# Bài toán CVRP
# K xe (mỗi xe có tải trọng Q)
# Tìm lộ trình cho K xe (mỗi xe có sức chứa nhất định), mỗi xe đi đến chăm sóc
# một số khách hàng (mỗi khách hàng có nhu cầu lấy một lượng sản phẩm nhất định)
# sao cho Tổng tiền bỏ ra ít hơn với chi phí tối thiểu
# Các tham số:
#     n - Số khách hàng (n>1)
#     N - Tập các khách hàng (N = {1->n}. Tọa độ khách hàng (loc_x, loc_y)
#     Kho - {0}
#     V - Tập các đỉnh/node (V={0,1->n}
#     A - Tập các cung A = {(i,j) thuộc VxV: i khác j}
#     cij - Chi phí (khoảng cách) trên cung (i,j) thuộc A
#     Q - Tải trọng xe
#     qi - Tổng số sản phẩm phải được giao tính đến khách hàng i thuộc N


# Hàm mục tiêu
#     min (Tổng Cij.xij)với i,j thuộc A

# Các ràng buộc s.t.
#     1. (Tổng(xij) với j thuộc V, j khác i) = 1 với i thuộc N
#     2. (Tổng(xij) với i thuộc V, i khác j) = 1 với j thuộc N
#     3. Nếu xij=1 thì ui + qj = uj, với i,j thuộc A, j khác 0, i khác 0
#     4. qi<=ui<= Q, với i thuộc N
#     5. xij thuộc {0,1}, với i,j thuộc A

                           
a = [3,4,-1]
b = sorted(a)
step = 0
for i in a:
    index = b.index(i)
    if len(b[:index]) == 0:
        step += 1
        b.remove(i)
    elif len(b[index:]) == 1 and len(b[:index]) != 0:
        step += len(b[:index])
        b.remove(i)
    elif len(b[index:]) != 1 and len(b[:index]) != 0:
        step += (len(b[:index]) + len(b[index:]))
        b.remove(i)
    print(step,b)
print(step)