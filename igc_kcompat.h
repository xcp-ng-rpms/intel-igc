/* This file contains implementations of backports from various kernels.
 * Much of the code is from the out tree dirver igb of Intel Corporation.
 * Modified by Stephen Cheng from Cloud Software Group Inc for XenServer 8.
 * Because the XS8 kernel version is fixed (4.19),
 * no need to consider other kernel versions.
 */
#ifndef IGC_KCOMPAT_H_
#define IGC_KCOMPAT_H_

#include <linux/skbuff.h>
#include <linux/etherdevice.h>


/*
 * Upstream commit 361800876f80 ("ptp: add PTP_SYS_OFFSET_EXTENDED
 * ioctl") introduces new ioctl, driver and helper functions.
 *
 * Backport PTP patches introduced in Linux Kernel version 5.0 on 4.x kernels
 */
struct ptp_system_timestamp {
    struct timespec64 pre_ts;
    struct timespec64 post_ts;
};

static inline void
ptp_read_system_prets(struct ptp_system_timestamp *sts) { }

static inline void
ptp_read_system_postts(struct ptp_system_timestamp *sts) { }


/* GCC fallthrough support */
#ifdef __has_attribute
#if __has_attribute(__fallthrough__)
# define fallthrough __attribute__((__fallthrough__))
#else
# define fallthrough do {} while (0)  /* fallthrough */
#endif /* __has_attribute(fallthrough) */
#else
# define fallthrough do {} while (0)  /* fallthrough */
#endif /* __has_attribute */



/* NET_PREFETCH
 *
 * net_prefetch was introduced by commit f468f21b7af0 ("net: Take common
 * prefetch code structure into a function")
 *
 * This function is trivial to re-implement in full.
 */
static inline void net_prefetch(void *p)
{
	prefetch(p);
#if L1_CACHE_BYTES < 128
	prefetch((u8 *)p + L1_CACHE_BYTES);
#endif
}

/* eth_get_headlen only has two input arguments in kernel 4.19 */
#ifndef eth_get_headlen
static inline u32
__kc_eth_get_headlen(const struct net_device __always_unused *dev, void *data,
		     unsigned int len)
{
	return eth_get_headlen(data, len);
}

#define eth_get_headlen(dev, data, len) __kc_eth_get_headlen(dev, data, len)
#endif /* !eth_get_headlen */

/* From kenel version 5.2 */
#define netdev_xmit_more()	(skb->xmit_more)

/* net: add inline function skb_csum_is_sctp
* This function was introduced by commit fa82117010430aff2ce86400f7328f55a31b48a6
*/
static inline bool skb_csum_is_sctp(struct sk_buff *skb)
{
	return skb->csum_not_inet;
}

/* Rename DPM_FLAG_NEVER_SKIP to DPM_FLAG_NO_DIRECT_COMPLETE
 * Introduced by commit e07515563d010d8b32967634e8dc2fdc732c1aa6
*/
#ifndef DPM_FLAG_NO_DIRECT_COMPLETE
#define DPM_FLAG_NO_DIRECT_COMPLETE DPM_FLAG_NEVER_SKIP
#endif

#endif /* IGC_KCOMPAT_H_ */